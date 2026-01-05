import React, { useEffect } from 'react';

const ChatWidget = () => {
  useEffect(() => {
    // 1. Add the CSS to the head
    const link = document.createElement('link');
    link.href = 'https://cdn.jsdelivr.net/npm/@n8n/chat/dist/style.css';
    link.rel = 'stylesheet';
    document.head.appendChild(link);

    // 2. Load the modern ES bundle
    const script = document.createElement('script');
    script.type = 'module'; // Critical for the new version
    script.innerHTML = `
      import { createChat } from 'https://cdn.jsdelivr.net/npm/@n8n/chat/dist/chat.bundle.es.js';
      createChat({
        webhookUrl: 'https://www.n8n-hajruuudin.xyz/webhook/ae76ce14-17ab-4bfb-9008-18a814c80cbd/chat'
      });
    `;
    document.body.appendChild(script);

    return () => {
      document.head.removeChild(link);
      document.body.removeChild(script);
    };
  }, []);

  return <div id="n8n-chat"></div>;
};

export default ChatWidget;