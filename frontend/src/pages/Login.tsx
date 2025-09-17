import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { MessageCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function Login() {
  const [identity, setIdentity] = useState('');
  const [room, setRoom] = useState('default');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!identity.trim() || !room.trim()) return;
    
    setIsLoading(true);
    
    try {
      // Store identity and room in localStorage
      localStorage.setItem('chat-identity', identity.trim());
      localStorage.setItem('chat-room', room.trim());
      
      // Navigate to chat room
      navigate('/chat');
    } catch (error) {
      console.error('Login error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-chat-background flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center space-y-4">
          <div className="flex justify-center">
            <div className={cn(
              "w-16 h-16 bg-primary rounded-2xl flex items-center justify-center",
              "shadow-lg shadow-primary/20"
            )}>
              <MessageCircle className="w-8 h-8 text-primary-foreground" />
            </div>
          </div>
          <div className="space-y-2">
            <h1 className="text-3xl font-bold text-foreground">AI Chat</h1>
            <p className="text-muted-foreground">Enter your display name to start chatting</p>
          </div>
        </div>

        <Card className="border-border bg-card/50 backdrop-blur-sm shadow-xl">
          <CardHeader className="space-y-1">
            <CardTitle className="text-xl font-semibold text-center">Join Chat Room</CardTitle>
            <CardDescription className="text-center">
              Choose a display name to identify yourself in the chat
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Input
                  type="text"
                  placeholder="Enter your display name"
                  value={identity}
                  onChange={(e) => setIdentity(e.target.value)}
                  disabled={isLoading}
                  className={cn(
                    "bg-background border-border text-foreground",
                    "focus:ring-2 focus:ring-primary focus:border-transparent",
                    "transition-all duration-200",
                    "placeholder:text-muted-foreground"
                  )}
                  autoFocus
                />
              </div>
              <div className="space-y-2">
                <Input
                  type="text"
                  placeholder="Enter room name (e.g., default)"
                  value={room}
                  onChange={(e) => setRoom(e.target.value)}
                  disabled={isLoading}
                  className={cn(
                    "bg-background border-border text-foreground",
                    "focus:ring-2 focus:ring-primary focus:border-transparent",
                    "transition-all duration-200",
                    "placeholder:text-muted-foreground"
                  )}
                />
              </div>
              <Button
                type="submit"
                disabled={!identity.trim() || !room.trim() || isLoading}
                className={cn(
                  "w-full bg-primary hover:bg-primary/90 text-primary-foreground",
                  "transition-all duration-200 shadow-lg",
                  "disabled:opacity-50 disabled:cursor-not-allowed",
                  !isLoading && identity.trim() && room.trim() && "shadow-primary/20 hover:shadow-primary/30"
                )}
              >
                {isLoading ? (
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-primary-foreground/20 border-t-primary-foreground rounded-full animate-spin" />
                    Joining...
                  </div>
                ) : (
                  'Join Chat Room'
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        <div className="text-center text-sm text-muted-foreground">
          <p>Your messages will be visible to other participants in the room.</p>
        </div>
      </div>
    </div>
  );
}