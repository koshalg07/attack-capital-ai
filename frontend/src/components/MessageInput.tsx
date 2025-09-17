import { useState, useRef, KeyboardEvent } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export function MessageInput({ onSendMessage, disabled }: MessageInputProps) {
  const [message, setMessage] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSend = () => {
    if (!message.trim() || disabled) return;
    
    onSendMessage(message.trim());
    setMessage('');
    inputRef.current?.focus();
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-border bg-chat-input p-4">
      <div className="flex gap-3 max-w-4xl mx-auto">
        <div className="flex-1 relative">
          <Input
            ref={inputRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={disabled}
            className={cn(
              "bg-background border-border text-foreground",
              "focus:ring-2 focus:ring-primary focus:border-transparent",
              "transition-all duration-200 pr-12",
              "placeholder:text-muted-foreground"
            )}
          />
        </div>
        <Button
          onClick={handleSend}
          disabled={!message.trim() || disabled}
          size="icon"
          className={cn(
            "bg-primary hover:bg-primary/90 text-primary-foreground",
            "transition-all duration-200 shadow-lg",
            "disabled:opacity-50 disabled:cursor-not-allowed",
            !disabled && message.trim() && "shadow-primary/20 hover:shadow-primary/30"
          )}
        >
          <Send className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}