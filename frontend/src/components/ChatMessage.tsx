import { format } from 'date-fns';
import { ChatMessage as ChatMessageType } from '@/hooks/useLivekitChat';
import { cn } from '@/lib/utils';

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const formatTime = (timestamp: Date) => {
    return format(timestamp, 'HH:mm');
  };

  return (
    <div className={cn(
      "flex w-full mb-4 animate-in slide-in-from-bottom-2 duration-300",
      message.isUser ? "justify-end" : "justify-start"
    )}>
      <div className={cn(
        "max-w-[80%] rounded-lg px-4 py-3 shadow-lg",
        "transition-all duration-200 hover:shadow-xl",
        message.isUser 
          ? "bg-chat-user text-white rounded-br-sm" 
          : "bg-chat-assistant border border-border rounded-bl-sm"
      )}>
        <div className="flex items-start gap-2">
          <div className="flex-1">
            <div className={cn(
              "text-xs font-medium mb-1 opacity-80",
              message.isUser ? "text-primary-foreground" : "text-muted-foreground"
            )}>
              {message.sender}
            </div>
            <div className={cn(
              "text-sm leading-relaxed break-words",
              message.isUser ? "text-primary-foreground" : "text-foreground"
            )}>
              {message.content}
            </div>
          </div>
        </div>
        <div className={cn(
          "text-xs mt-2 opacity-60 text-right",
          message.isUser ? "text-primary-foreground" : "text-muted-foreground"
        )}>
          {formatTime(message.timestamp)}
        </div>
      </div>
    </div>
  );
}