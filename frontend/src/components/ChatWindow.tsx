import { useEffect, useRef } from 'react';
import { ChatMessage } from './ChatMessage';
import { ChatMessage as ChatMessageType } from '@/hooks/useLivekitChat';

interface ChatWindowProps {
  messages: ChatMessageType[];
  isTyping: boolean;
}

export function ChatWindow({ messages, isTyping }: ChatWindowProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  return (
    <div className="flex-1 overflow-hidden bg-chat-background">
      <div className="h-full overflow-y-auto px-4 py-6 space-y-1">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center text-muted-foreground">
              <div className="text-lg font-medium mb-2">Welcome to the chat!</div>
              <div className="text-sm opacity-80">Start a conversation by typing a message below.</div>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            
            {isTyping && (
              <div className="flex justify-start mb-4 animate-in slide-in-from-bottom-2 duration-300">
                <div className="bg-chat-assistant border border-border rounded-lg rounded-bl-sm px-4 py-3 shadow-lg">
                  <div className="text-xs font-medium mb-1 text-muted-foreground opacity-80">
                    Assistant
                  </div>
                  <div className="flex items-center gap-1">
                    <span className="text-sm text-chat-typing">Assistant is typing</span>
                    <div className="flex gap-1 ml-2">
                      <div className="w-1 h-1 bg-chat-typing rounded-full typing-dot"></div>
                      <div className="w-1 h-1 bg-chat-typing rounded-full typing-dot"></div>
                      <div className="w-1 h-1 bg-chat-typing rounded-full typing-dot"></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}