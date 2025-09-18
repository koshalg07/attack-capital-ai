import { useState, useEffect, useCallback, useRef } from 'react';
import { Room, RoomEvent, DataPacket_Kind, RemoteParticipant } from 'livekit-client';
import axios from 'axios';

export interface ChatMessage {
  id: string;
  sender: string;
  content: string;
  timestamp: Date;
  isUser: boolean;
}

interface UseLivekitChatProps {
  identity: string;
  room: string;
  onError?: (error: string) => void;
}

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:3001';

const AGENT_IDENTITY = import.meta.env.VITE_AGENT_IDENTITY || 'assistant';

export function useLivekitChat({ identity, room: roomName, onError }: UseLivekitChatProps) {
  const [room, setRoom] = useState<Room | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  
  const typingTimeoutRef = useRef<NodeJS.Timeout>();
  const agentJoinedRef = useRef<boolean>(false);
  const roomRef = useRef<Room | null>(null);
  const connectingRef = useRef<boolean>(false);

  const addMessage = useCallback((sender: string, content: string, isUser = false) => {
    const message: ChatMessage = {
      id: `${Date.now()}-${Math.random()}`,
      sender,
      content,
      timestamp: new Date(),
      isUser,
    };
    setMessages(prev => [...prev, message]);
  }, []);

  const connect = useCallback(async () => {
    if (connectingRef.current || roomRef.current || isConnecting || isConnected) return;
    
    setIsConnecting(true);
    connectingRef.current = true;
    try {
      // Get token from backend
      const response = await axios.get(`${BACKEND_URL}/token`, {
        params: { identity, room: roomName }
      });
      
      const { token, wsUrl } = response.data;
      
      // Create and connect to room
      const newRoom = new Room();
      
      // Minimal listeners + presence
      newRoom.on(RoomEvent.Connected, () => {
        console.log('Connected to room');
        setIsConnected(true);
        setIsConnecting(false);
        connectingRef.current = false;
        roomRef.current = newRoom;
      });

      newRoom.on(RoomEvent.Disconnected, () => {
        console.log('Disconnected from room');
        setIsConnected(false);
        setIsConnecting(false);
        connectingRef.current = false;
        roomRef.current = null;
      });

      newRoom.on(RoomEvent.DataReceived, (payload: Uint8Array, participant?: RemoteParticipant, kind?: DataPacket_Kind, topic?: string) => {
        if (topic === 'lk.chat') {
          const message = new TextDecoder().decode(payload);
          const senderName = participant?.identity || 'Assistant';
          addMessage(senderName, message, false);
          
          // Reset typing indicator
          setIsTyping(false);
          if (typingTimeoutRef.current) {
            clearTimeout(typingTimeoutRef.current);
          }
        }
      });

      newRoom.on(RoomEvent.ParticipantConnected, (participant) => {
        addMessage('System', `${participant.identity} joined the room`, false);
      });

      console.log('Connecting to LiveKit:', wsUrl);
      await newRoom.connect(wsUrl, token, {
        rtcConfig: {
          iceTransportPolicy: 'relay',
        },
        autoSubscribe: true,
      });
      // RoomEvent.Connected handler will flip state
      setRoom(newRoom);
      roomRef.current = newRoom;

      // List already present participants (besides self)
      Array.from(newRoom.remoteParticipants.values()).forEach((p) => {
        addMessage('System', `${p.identity} is in the room`, false);
      });
      
    } catch (error) {
      console.error('Failed to connect:', error);
      onError?.('Failed to connect to chat room');
      setIsConnecting(false);
      connectingRef.current = false;
    }
  }, [identity, roomName, isConnecting, isConnected, onError, addMessage]);

  const sendMessage = useCallback(async (message: string) => {
    if (!room || !isConnected || !message.trim()) return;

    try {
      // Send message to data channel
      const encoder = new TextEncoder();
      const data = encoder.encode(message);
      await room.localParticipant.publishData(data, { topic: 'lk.chat' });
      
      // Add to local messages
      addMessage(identity, message, true);
      
      // Show typing indicator for assistant response
      setIsTyping(true);
      
      // Set timeout to hide typing indicator if no response
      if (typingTimeoutRef.current) {
        clearTimeout(typingTimeoutRef.current);
      }
      typingTimeoutRef.current = setTimeout(() => {
        setIsTyping(false);
      }, 10000); // 10 seconds timeout
      
      // Also ask backend agent for a reply and append it
      try {
        const resp = await axios.post(`${BACKEND_URL}/agent/reply`, {
          userId: identity,
          text: message,
        });
        const reply: string = resp.data?.reply ?? "";
        if (reply) {
          addMessage('Assistant', reply, false);
          setIsTyping(false);
        }
      } catch (e) {
        console.error('Agent reply failed', e);
        setIsTyping(false);
      }

    } catch (error) {
      console.error('Failed to send message:', error);
      onError?.('Failed to send message');
    }
  }, [room, isConnected, identity, addMessage, onError]);

  const disconnect = useCallback(() => {
    if (room) {
      room.disconnect();
      setRoom(null);
    }
    setIsConnected(false);
    setIsConnecting(false);
    setMessages([]);
    
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
    }
  }, [room]);

  useEffect(() => {
    return () => {
      // no-op: avoid auto-disconnect to prevent churn
    };
  }, []);

  return {
    connect,
    disconnect,
    sendMessage,
    messages,
    isConnected,
    isConnecting,
    isTyping,
  };
}