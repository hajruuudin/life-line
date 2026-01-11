// FRONTEND TEST 1: Header Component
//
// What we're testing: The Header component
// Why: Header is displayed on every page - critical to test it works
//
// Location: src/__tests__/components/Header.test.jsx
// Component: src/components/Header.jsx

import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Header from '../../components/Header'

// Group all Header tests together with describe()
describe('Header Component', () => {
  // TEST 1.1: Component renders without crashing
  it('should render without crashing', () => {
    // Arrange: Create a mock function for onLogout
    const mockOnLogout = vi.fn()

    // Act: Render the component
    render(<Header onLogout={mockOnLogout} />)

    // Assert: Component should not throw any errors
    expect(screen.getByText('LIFELINE')).toBeInTheDocument()
  })

  // TEST 1.2: Component displays LIFELINE logo
  it('should display LIFELINE text', () => {
    // Arrange: Create a mock function
    const mockOnLogout = vi.fn()

    // Act: Render the component
    render(<Header onLogout={mockOnLogout} />)

    // Assert: Check that LIFELINE text is visible
    const logoText = screen.getByText('LIFELINE')
    expect(logoText).toBeInTheDocument()
  })

  // TEST 1.3: Component has logout button
  it('should have a logout button', () => {
    // Arrange: Create a mock function
    const mockOnLogout = vi.fn()

    // Act: Render the component
    render(<Header onLogout={mockOnLogout} />)

    // Assert: Check that logout button exists
    const logoutButton = screen.getByRole('button', { name: /logout/i })
    expect(logoutButton).toBeInTheDocument()
  })

  // TEST 1.4: Logout button calls onLogout when clicked
  it('should call onLogout when logout button is clicked', async () => {
    // Arrange: Create a mock function to track calls
    const mockOnLogout = vi.fn()

    // Act: Render component and simulate user clicking logout
    render(<Header onLogout={mockOnLogout} />)
    const logoutButton = screen.getByRole('button', { name: /logout/i })

    // Simulate user clicking the button
    const user = userEvent.setup()
    await user.click(logoutButton)

    // Assert: Verify onLogout was called exactly once
    expect(mockOnLogout).toHaveBeenCalledOnce()
  })

  // TEST 1.5: Logout button is clickable (not disabled)
  it('should have logout button enabled', () => {
    // Arrange
    const mockOnLogout = vi.fn()

    // Act: Render component
    render(<Header onLogout={mockOnLogout} />)
    const logoutButton = screen.getByRole('button', { name: /logout/i })

    // Assert: Button should not be disabled
    expect(logoutButton).not.toBeDisabled()
  })
})
