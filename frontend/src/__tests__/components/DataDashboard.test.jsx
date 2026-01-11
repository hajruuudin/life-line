import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import DataDashboard from '../../components/DataDashboard';
import * as medicationsService from '../../services/medications';

vi.mock('../../services/medications');
vi.mock('../../components/DriveSection', () => ({
  default: () => <div data-testid="drive-section">DriveSection</div>,
}));
vi.mock('../../components/InventoryTable', () => ({
  default: ({ medications, onDataChange }) => (
    <div data-testid="inventory-table">
      InventoryTable - {medications?.length || 0} items
      <button onClick={() => onDataChange?.()}>Trigger Change</button>
    </div>
  ),
}));

describe('DataDashboard Component', () => {
  it('should render the dashboard section', () => {
    const { container } = render(<DataDashboard medications={[]} onDataChange={() => {}} />);
    const dashboard = container.querySelector('.data-dashboard');
    expect(dashboard).toBeInTheDocument();
  });

  it('should have the correct CSS class on dashboard', () => {
    const { container } = render(<DataDashboard medications={[]} onDataChange={() => {}} />);
    const dashboard = container.querySelector('.data-dashboard');
    expect(dashboard).toHaveClass('data-dashboard');
  });

  it('should render a dashboard row', () => {
    const { container } = render(<DataDashboard medications={[]} onDataChange={() => {}} />);
    const row = container.querySelector('.dashboard-row');
    expect(row).toBeInTheDocument();
  });

  it('should render two dashboard columns', () => {
    const { container } = render(<DataDashboard medications={[]} onDataChange={() => {}} />);
    const columns = container.querySelectorAll('.dashboard-column');
    expect(columns).toHaveLength(2);
  });

  it('should render DriveSection component', () => {
    render(<DataDashboard medications={[]} onDataChange={() => {}} />);
    const driveSection = screen.getByTestId('drive-section');
    expect(driveSection).toBeInTheDocument();
  });

  it('should render InventoryTable component', () => {
    render(<DataDashboard medications={[]} onDataChange={() => {}} />);
    const inventoryTable = screen.getByTestId('inventory-table');
    expect(inventoryTable).toBeInTheDocument();
  });

  it('should pass medications prop to InventoryTable', () => {
    const medications = [
      { id: 1, name: 'Aspirin', quantity: 10 },
      { id: 2, name: 'Ibuprofen', quantity: 5 },
    ];
    render(<DataDashboard medications={medications} onDataChange={() => {}} />);
    const inventoryTable = screen.getByTestId('inventory-table');
    expect(inventoryTable).toHaveTextContent('2 items');
  });

  it('should pass onDataChange callback to InventoryTable', () => {
    const onDataChange = vi.fn();
    render(<DataDashboard medications={[]} onDataChange={onDataChange} />);
    const button = screen.getByText('Trigger Change');
    button.click();
    expect(onDataChange).toHaveBeenCalled();
  });

  it('should render with empty medications array', () => {
    render(<DataDashboard medications={[]} onDataChange={() => {}} />);
    const inventoryTable = screen.getByTestId('inventory-table');
    expect(inventoryTable).toHaveTextContent('0 items');
  });

  it('should render with multiple medications', () => {
    const medications = Array.from({ length: 5 }, (_, i) => ({
      id: i + 1,
      name: `Med ${i + 1}`,
      quantity: 10,
    }));
    render(<DataDashboard medications={medications} onDataChange={() => {}} />);
    const inventoryTable = screen.getByTestId('inventory-table');
    expect(inventoryTable).toHaveTextContent('5 items');
  });

  it('should place DriveSection in first column', () => {
    const { container } = render(<DataDashboard medications={[]} onDataChange={() => {}} />);
    const columns = container.querySelectorAll('.dashboard-column');
    const firstColumn = columns[0];
    const driveSection = firstColumn.querySelector('[data-testid="drive-section"]');
    expect(driveSection).toBeInTheDocument();
  });

  it('should place InventoryTable in second column', () => {
    const { container } = render(<DataDashboard medications={[]} onDataChange={() => {}} />);
    const columns = container.querySelectorAll('.dashboard-column');
    const secondColumn = columns[1];
    const inventoryTable = secondColumn.querySelector('[data-testid="inventory-table"]');
    expect(inventoryTable).toBeInTheDocument();
  });
});
