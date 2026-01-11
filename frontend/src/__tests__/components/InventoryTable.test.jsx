// FRONTEND TEST 3: InventoryTable Component
//
// What we're testing: The InventoryTable component
// Why: Complex component with conditional rendering, status logic, and delete functionality
//
// Key logic to test:
// - Empty state when no medications
// - Table displays medications
// - Status indicators (In Stock, Low Stock, Expired)
// - Quantity warnings for low stock
// - Delete button works

import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import InventoryTable from '../../components/InventoryTable'

describe('InventoryTable Component', () => {
  const mockOnDataChange = vi.fn()

  // TEST 3.1: Empty state shows when no medications
  it('should show empty state when no medications exist', () => {
    // Arrange
    render(
      <InventoryTable
        medications={[]}
        onDataChange={mockOnDataChange}
      />
    )

    // Act & Assert
    expect(screen.getByText('Inventory is empty')).toBeInTheDocument()
    expect(screen.getByText(/Add your first medication to get started/i)).toBeInTheDocument()
  })

  // TEST 3.2: Table renders when medications exist
  it('should render table with medications', () => {
    // Arrange
    const futureDate = new Date()
    futureDate.setDate(futureDate.getDate() + 30)
    
    const medications = [
      {
        id: 1,
        name: 'Aspirin',
        quantity: 50,
        expiration_date: futureDate.toISOString()
      }
    ]

    render(
      <InventoryTable
        medications={medications}
        onDataChange={mockOnDataChange}
      />
    )

    // Act & Assert
    expect(screen.getByText('Aspirin')).toBeInTheDocument()
    expect(screen.getByText('50')).toBeInTheDocument()
  })

  // TEST 3.3: In Stock status shows for normal quantities
  it('should show In Stock status for medications with quantity >= 10', () => {
    // Arrange - Use full ISO date format with time
    const futureDate = new Date()
    futureDate.setDate(futureDate.getDate() + 30) // 30 days in future
    
    const medications = [
      {
        id: 1,
        name: 'Aspirin',
        quantity: 50,
        expiration_date: futureDate.toISOString()
      }
    ]

    render(
      <InventoryTable
        medications={medications}
        onDataChange={mockOnDataChange}
      />
    )

    // Act & Assert - Check for any status pill that's not expired
    const statusPills = screen.getAllByRole('cell')
    // Find a status pill that contains text
    const inStockFound = statusPills.some(el => el.textContent.includes('In Stock'))
    expect(inStockFound).toBe(true)
  })

  // TEST 3.4: Low Stock status shows when quantity < 10
  it('should show Low Stock status when quantity is less than 10', () => {
    // Arrange - Use full ISO date format with time
    const futureDate = new Date()
    futureDate.setDate(futureDate.getDate() + 30) // 30 days in future
    
    const medications = [
      {
        id: 1,
        name: 'Aspirin',
        quantity: 5,
        expiration_date: futureDate.toISOString()
      }
    ]

    render(
      <InventoryTable
        medications={medications}
        onDataChange={mockOnDataChange}
      />
    )

    // Act & Assert - Check for low stock status
    const statusPills = screen.getAllByRole('cell')
    const lowStockFound = statusPills.some(el => el.textContent.includes('Low Stock'))
    expect(lowStockFound).toBe(true)
  })

  // TEST 3.5: Expired status shows for past expiration dates
  it('should show Expired status when expiration date is in the past', () => {
    // Arrange - Use a past date
    const medications = [
      {
        id: 1,
        name: 'Aspirin',
        quantity: 50,
        expiration_date: '2020-01-01'
      }
    ]

    render(
      <InventoryTable
        medications={medications}
        onDataChange={mockOnDataChange}
      />
    )

    // Act & Assert
    expect(screen.getByText('Expired')).toBeInTheDocument()
  })

  // TEST 3.6: Multiple medications display correctly
  it('should display multiple medications in table', () => {
    // Arrange
    const futureDate = new Date()
    futureDate.setDate(futureDate.getDate() + 30)
    
    const medications = [
      {
        id: 1,
        name: 'Aspirin',
        quantity: 50,
        expiration_date: futureDate.toISOString()
      },
      {
        id: 2,
        name: 'Ibuprofen',
        quantity: 30,
        expiration_date: futureDate.toISOString()
      },
      {
        id: 3,
        name: 'Paracetamol',
        quantity: 5,
        expiration_date: futureDate.toISOString()
      }
    ]

    render(
      <InventoryTable
        medications={medications}
        onDataChange={mockOnDataChange}
      />
    )

    // Act & Assert - All medications should be visible
    expect(screen.getByText('Aspirin')).toBeInTheDocument()
    expect(screen.getByText('Ibuprofen')).toBeInTheDocument()
    expect(screen.getByText('Paracetamol')).toBeInTheDocument()

    // Check quantities
    expect(screen.getByText('50')).toBeInTheDocument()
    expect(screen.getByText('30')).toBeInTheDocument()
    expect(screen.getByText('5')).toBeInTheDocument()
  })

  // TEST 3.7: Add Item button exists
  it('should have Add Item button in table view', () => {
    // Arrange
    const futureDate = new Date()
    futureDate.setDate(futureDate.getDate() + 30)
    
    const medications = [
      {
        id: 1,
        name: 'Aspirin',
        quantity: 50,
        expiration_date: futureDate.toISOString()
      }
    ]

    render(
      <InventoryTable
        medications={medications}
        onDataChange={mockOnDataChange}
      />
    )

    // Act & Assert
    const addButton = screen.getByRole('button', { name: /add item/i })
    expect(addButton).toBeInTheDocument()
  })

  // TEST 3.8: Add Medication button exists in empty state
  it('should have Add Medication button in empty state', () => {
    // Arrange
    render(
      <InventoryTable
        medications={[]}
        onDataChange={mockOnDataChange}
      />
    )

    // Act & Assert
    const addButton = screen.getByRole('button', { name: /add medication/i })
    expect(addButton).toBeInTheDocument()
  })

  // TEST 3.9: Table headers are correct
  it('should display correct table headers', () => {
    // Arrange
    const futureDate = new Date()
    futureDate.setDate(futureDate.getDate() + 30)
    
    const medications = [
      {
        id: 1,
        name: 'Aspirin',
        quantity: 50,
        expiration_date: futureDate.toISOString()
      }
    ]

    render(
      <InventoryTable
        medications={medications}
        onDataChange={mockOnDataChange}
      />
    )

    // Act & Assert - Check for table headers
    expect(screen.getByText('Name')).toBeInTheDocument()
    expect(screen.getByText('Quantity')).toBeInTheDocument()
    expect(screen.getByText('Status')).toBeInTheDocument()
  })

  // TEST 3.10: Delete button shows for each medication
  it('should have delete button for each medication', () => {
    // Arrange
    const futureDate = new Date()
    futureDate.setDate(futureDate.getDate() + 30)
    
    const medications = [
      {
        id: 1,
        name: 'Aspirin',
        quantity: 50,
        expiration_date: futureDate.toISOString()
      },
      {
        id: 2,
        name: 'Ibuprofen',
        quantity: 30,
        expiration_date: futureDate.toISOString()
      }
    ]

    render(
      <InventoryTable
        medications={medications}
        onDataChange={mockOnDataChange}
      />
    )

    // Act & Assert - Should have 2 delete buttons (one per medication)
    const deleteButtons = screen.getAllByRole('button', { name: '' })
    expect(deleteButtons.length).toBeGreaterThanOrEqual(2)
  })
})
