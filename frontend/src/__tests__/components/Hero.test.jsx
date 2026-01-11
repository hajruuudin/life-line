import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Hero from '../../components/Hero';

describe('Hero Component', () => {
  it('should render the hero section', () => {
    const { container } = render(<Hero />);
    const heroSection = container.querySelector('.hero-section');
    expect(heroSection).toBeInTheDocument();
  });

  it('should have the correct HTML tag for hero section', () => {
    const { container } = render(<Hero />);
    const heroSection = container.querySelector('section.hero-section');
    expect(heroSection).toBeInTheDocument();
  });

  it('should display the hero title "Welcome to LIFELINE"', () => {
    render(<Hero />);
    const title = screen.getByRole('heading', { level: 2 });
    expect(title).toHaveTextContent('Welcome to LIFELINE');
  });

  it('should have the correct CSS class on hero title', () => {
    render(<Hero />);
    const title = screen.getByRole('heading', { level: 2 });
    expect(title).toHaveClass('hero-title');
  });

  it('should display the hero subtitle with correct content', () => {
    render(<Hero />);
    const subtitle = screen.getByText(/Track your family's health, manage medications, and stay organized with your health records./);
    expect(subtitle).toBeInTheDocument();
  });

  it('should have the correct CSS class on hero subtitle', () => {
    render(<Hero />);
    const subtitle = screen.getByText(/Track your family's health, manage medications, and stay organized with your health records./);
    expect(subtitle).toHaveClass('hero-subtitle');
  });

  it('should render exactly one heading element', () => {
    render(<Hero />);
    const headings = screen.getAllByRole('heading');
    expect(headings).toHaveLength(1);
  });

  it('should render the subtitle as a paragraph element', () => {
    const { container } = render(<Hero />);
    const paragraph = container.querySelector('p.hero-subtitle');
    expect(paragraph).toBeInTheDocument();
  });
});
