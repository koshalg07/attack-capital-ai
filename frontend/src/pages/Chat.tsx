import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLivekitChat } from '@/hooks/useLivekitChat';
import { ChatWindow } from '@/components/ChatWindow';
import { MessageInput } from '@/components/MessageInput';
import { Button } from '@/components/ui/button';
import { LogOut, MessageCircle, Wifi, WifiOff } from 'lucide-react';
import { toast } from '@/hooks/use-toast';
import { cn } from '@/lib/utils';

export default function Chat() {
  const [identity, setIdentity] = useState<string>('');
  const [room, setRoom] = useState<string>('');
  const navigate = useNavigate();

  const {
    connect,
    disconnect,
    sendMessage,
    messages,
    isConnected,
    isConnecting,
    isTyping,
  } = useLivekitChat({
    identity,
    room,
    onError: (error) => {
      toast({
        title: 'Connection Error',
        description: error,
        variant: 'destructive',
      });
    },
  });

  useEffect(() => {
    const savedIdentity = localStorage.getItem('chat-identity');
    const savedRoom = localStorage.getItem('chat-room');
    if (!savedIdentity || !savedRoom) {
      navigate('/');
      return;
    }
    
    setIdentity(savedIdentity);
    setRoom(savedRoom);
  }, [navigate]);

  useEffect(() => {
    if (identity && !isConnected && !isConnecting) {
      connect();
    }
  }, [identity, isConnected, isConnecting, connect]);

  const handleLeave = () => {
    disconnect();
    localStorage.removeItem('chat-identity');
    localStorage.removeItem('chat-room');
    navigate('/');
  };

  const connectionStatus = isConnecting ? 'Connecting...' : isConnected ? 'Connected' : 'Disconnected';
  const StatusIcon = isConnecting ? Wifi : isConnected ? Wifi : WifiOff;

  return (
    <div className="min-h-screen bg-chat-background flex flex-col">
      {/* Header */}
      <header className="border-b border-border bg-card/80 backdrop-blur-sm">
        <div className="flex items-center justify-between px-4 py-3">
          <div className="flex items-center gap-3">
            <div className={cn(
              "w-10 h-10 bg-primary rounded-xl flex items-center justify-center",
              "shadow-lg shadow-primary/20"
            )}>
              <MessageCircle className="w-5 h-5 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-lg font-semibold text-foreground">AI Chat Room</h1>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <StatusIcon className={cn(
                  "w-3 h-3",
                  isConnected ? "text-green-500" : isConnecting ? "text-yellow-500" : "text-red-500"
                )} />
                <span>{connectionStatus}</span>
                {identity && (
                  <>
                    <span>•</span>
                    <span>Logged in as {identity}</span>
                  </>
                )}
                {room && (
                  <>
                    <span>•</span>
                    <span>Room: {room}</span>
                  </>
                )}
              </div>
            </div>
          </div>
          
          <Button
            variant="outline"
            size="sm"
            onClick={handleLeave}
            className="border-border hover:bg-destructive hover:text-destructive-foreground hover:border-destructive"
          >
            <LogOut className="w-4 h-4 mr-2" />
            Leave
          </Button>
        </div>
      </header>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col min-h-0">
        <ChatWindow messages={messages} isTyping={isTyping} />
        <MessageInput 
          onSendMessage={sendMessage} 
          disabled={!isConnected || isConnecting}
        />
      </div>
    </div>
  );
}