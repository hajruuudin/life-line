import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import ChatWidget from '../../components/ChatWidget';

describe('ChatWidget Component', () => {
  beforeEach(() => {
    vi.spyOn(document, 'createElement');
    vi.spyOn(document.head, 'appendChild');
    vi.spyOn(document.body, 'appendChild');
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('should render the chat widget div', () => {
    const { container } = render(<ChatWidget />);
    const chatDiv = container.querySelector('#n8n-chat');
    expect(chatDiv).toBeInTheDocument();
  });

  it('should have the correct id on chat container', () => {
    const { container } = render(<ChatWidget />);
    const chatDiv = container.querySelector('#n8n-chat');
    expect(chatDiv).toHaveAttribute('id', 'n8n-chat');
  });

  it('should add CSS link to document head', () => {
    render(<ChatWidget />);
    const links = document.head.querySelectorAll('link');
    const chatLink = Array.from(links).find((link) =>
      link.href.includes('@n8n/chat') && link.href.includes('style.css')
    );
    expect(chatLink).toBeDefined();
  });

  it('should set link rel attribute to stylesheet', () => {
    render(<ChatWidget />);
    const links = document.head.querySelectorAll('link');
    const chatLink = Array.from(links).find((link) =>
      link.href.includes('@n8n/chat') && link.href.includes('style.css')
    );
    expect(chatLink?.rel).toBe('stylesheet');
  });

  it('should add script to document body', () => {
    render(<ChatWidget />);
    const scripts = document.body.querySelectorAll('script');
    const chatScript = Array.from(scripts).find(
      (script) => script.type === 'module' && script.innerHTML.includes('createChat')
    );
    expect(chatScript).toBeDefined();
  });

  it('should set script type to module', () => {
    render(<ChatWidget />);
    const scripts = document.body.querySelectorAll('script');
    const chatScript = Array.from(scripts).find(
      (script) => script.type === 'module' && script.innerHTML.includes('createChat')
    );
    expect(chatScript?.type).toBe('module');
  });

  it('should import from n8n chat bundle', () => {
    render(<ChatWidget />);
    const scripts = document.body.querySelectorAll('script');
    const chatScript = Array.from(scripts).find(
      (script) => script.type === 'module' && script.innerHTML.includes('createChat')
    );
    expect(chatScript?.innerHTML).toContain('@n8n/chat');
    expect(chatScript?.innerHTML).toContain('chat.bundle.es.js');
  });

  it('should configure webhook URL', () => {
    render(<ChatWidget />);
    const scripts = document.body.querySelectorAll('script');
    const chatScript = Array.from(scripts).find(
      (script) => script.type === 'module' && script.innerHTML.includes('createChat')
    );
    expect(chatScript?.innerHTML).toContain('webhookUrl');
    expect(chatScript?.innerHTML).toContain('n8n-hajruuudin.xyz');
  });

  it('should enable welcome screen', () => {
    render(<ChatWidget />);
    const scripts = document.body.querySelectorAll('script');
    const chatScript = Array.from(scripts).find(
      (script) => script.type === 'module' && script.innerHTML.includes('createChat')
    );
    expect(chatScript?.innerHTML).toContain('showWelcomeScreen: true');
  });

  it('should set initial assistant message', () => {
    render(<ChatWidget />);
    const scripts = document.body.querySelectorAll('script');
    const chatScript = Array.from(scripts).find(
      (script) => script.type === 'module' && script.innerHTML.includes('createChat')
    );
    expect(chatScript?.innerHTML).toContain('LIFELINE assistant');
    expect(chatScript?.innerHTML).toContain('initialMessages');
  });

  it('should configure i18n English title', () => {
    render(<ChatWidget />);
    const scripts = document.body.querySelectorAll('script');
    const chatScript = Array.from(scripts).find(
      (script) => script.type === 'module' && script.innerHTML.includes('createChat')
    );
    expect(chatScript?.innerHTML).toContain('LIFELINE Assistant');
  });

  it('should cleanup link from head on unmount', () => {
    const { unmount } = render(<ChatWidget />);
    const linksBeforeUnmount = document.head.querySelectorAll('link').length;

    unmount();

    const linksAfterUnmount = document.head.querySelectorAll('link').length;
    expect(linksAfterUnmount).toBeLessThan(linksBeforeUnmount);
  });

  it('should cleanup script from body on unmount', () => {
    const { unmount } = render(<ChatWidget />);
    const scriptsBeforeUnmount = document.body.querySelectorAll('script[type="module"]').length;

    unmount();

    const scriptsAfterUnmount = document.body.querySelectorAll('script[type="module"]').length;
    expect(scriptsAfterUnmount).toBeLessThan(scriptsBeforeUnmount);
  });
});
