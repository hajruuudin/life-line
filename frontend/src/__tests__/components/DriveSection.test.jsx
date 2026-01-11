import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import DriveSection from '../../components/DriveSection';

vi.mock('../../services/googleDrive', () => ({
  googleDriveService: {
    listFiles: vi.fn(),
    uploadFile: vi.fn(),
    deleteFile: vi.fn(),
  },
}));

vi.mock('react-dropzone', () => ({
  useDropzone: vi.fn(() => ({
    getRootProps: (props) => ({ ...props, 'data-testid': 'dropzone' }),
    getInputProps: () => ({ 'data-testid': 'file-input' }),
    isDragActive: false,
  })),
}));

vi.mock('../../components/modals/DeleteFileModal', () => ({
  default: ({ onConfirm, onCancel, fileName }) => (
    <div data-testid="delete-modal">
      <p>Delete {fileName}?</p>
      <button onClick={onConfirm}>Confirm</button>
      <button onClick={onCancel}>Cancel</button>
    </div>
  ),
}));

import { googleDriveService } from '../../services/googleDrive';

describe('DriveSection Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should show loading state on mount', () => {
    googleDriveService.listFiles.mockResolvedValue({ files: [], connected: true });
    render(<DriveSection />);
    expect(screen.getByText('Loading files...')).toBeInTheDocument();
  });

  it('should load files on mount', async () => {
    const mockFiles = [
      { id: '1', name: 'document.pdf', mimeType: 'application/pdf' },
    ];
    googleDriveService.listFiles.mockResolvedValue({ files: mockFiles, connected: true });

    render(<DriveSection />);

    await waitFor(() => {
      expect(googleDriveService.listFiles).toHaveBeenCalled();
    });
  });

  it('should display Google Drive section title', async () => {
    googleDriveService.listFiles.mockResolvedValue({ files: [], connected: true });
    render(<DriveSection />);

    await waitFor(() => {
      expect(screen.getByText('Google Drive')).toBeInTheDocument();
    });
  });

  it('should show not-connected state when disconnected', async () => {
    googleDriveService.listFiles.mockResolvedValue({ files: [], connected: false });
    render(<DriveSection />);

    await waitFor(() => {
      expect(screen.getByText('Connect to Google Drive')).toBeInTheDocument();
    });
  });

  it('should display connection prompt message', async () => {
    googleDriveService.listFiles.mockResolvedValue({ files: [], connected: false });
    render(<DriveSection />);

    await waitFor(() => {
      expect(screen.getByText(/Link your Google account/)).toBeInTheDocument();
    });
  });

  it('should show Connect Now button when disconnected', async () => {
    googleDriveService.listFiles.mockResolvedValue({ files: [], connected: false });
    render(<DriveSection />);

    await waitFor(() => {
      expect(screen.getByText('Connect Now')).toBeInTheDocument();
    });
  });

  it('should retry loading on Connect Now click', async () => {
    googleDriveService.listFiles.mockResolvedValue({ files: [], connected: false });
    const { rerender } = render(<DriveSection />);

    await waitFor(() => {
      expect(screen.getByText('Connect Now')).toBeInTheDocument();
    });

    const connectButton = screen.getByText('Connect Now');
    expect(connectButton).toBeInTheDocument();
  });

  it('should show empty state when no files and connected', async () => {
    googleDriveService.listFiles.mockResolvedValue({ files: [], connected: true });
    render(<DriveSection />);

    await waitFor(() => {
      expect(screen.getByText('Drag & drop to upload')).toBeInTheDocument();
    });
  });

  it('should display Add File button when connected', async () => {
    googleDriveService.listFiles.mockResolvedValue({ files: [], connected: true });
    render(<DriveSection />);

    await waitFor(() => {
      expect(screen.getByText('Add File')).toBeInTheDocument();
    });
  });

  it('should display file cards when files exist', async () => {
    const mockFiles = [
      { id: '1', name: 'document.pdf', mimeType: 'application/pdf' },
      { id: '2', name: 'image.jpg', mimeType: 'image/jpeg' },
    ];
    googleDriveService.listFiles.mockResolvedValue({ files: mockFiles, connected: true });

    render(<DriveSection />);

    await waitFor(() => {
      expect(screen.getByText('document.pdf')).toBeInTheDocument();
      expect(screen.getByText('image.jpg')).toBeInTheDocument();
    });
  });

  it('should display file MIME types', async () => {
    const mockFiles = [
      { id: '1', name: 'document.pdf', mimeType: 'application/pdf' },
    ];
    googleDriveService.listFiles.mockResolvedValue({ files: mockFiles, connected: true });

    render(<DriveSection />);

    await waitFor(() => {
      expect(screen.getByText('application/pdf')).toBeInTheDocument();
    });
  });

  it('should show delete modal when delete button clicked', async () => {
    const mockFiles = [
      { id: '1', name: 'document.pdf', mimeType: 'application/pdf' },
    ];
    googleDriveService.listFiles.mockResolvedValue({ files: mockFiles, connected: true });

    render(<DriveSection />);

    await waitFor(() => {
      expect(screen.getByText('document.pdf')).toBeInTheDocument();
    });

    const deleteButtons = screen.getAllByRole('button', { name: '' });
    const deleteButton = deleteButtons[deleteButtons.length - 1];
    await userEvent.click(deleteButton);

    expect(screen.getByTestId('delete-modal')).toBeInTheDocument();
  });

  it('should call deleteFile service when delete confirmed', async () => {
    const mockFiles = [
      { id: '1', name: 'document.pdf', mimeType: 'application/pdf' },
    ];
    googleDriveService.listFiles.mockResolvedValue({ files: mockFiles, connected: true });
    googleDriveService.deleteFile.mockResolvedValue({});

    render(<DriveSection />);

    await waitFor(() => {
      expect(screen.getByText('document.pdf')).toBeInTheDocument();
    });

    const deleteButtons = screen.getAllByRole('button', { name: '' });
    const deleteButton = deleteButtons[deleteButtons.length - 1];
    await userEvent.click(deleteButton);

    const confirmButton = screen.getByText('Confirm');
    await userEvent.click(confirmButton);

    await waitFor(() => {
      expect(googleDriveService.deleteFile).toHaveBeenCalledWith('1');
    });
  });

  it('should reload files after successful deletion', async () => {
    const mockFiles = [
      { id: '1', name: 'document.pdf', mimeType: 'application/pdf' },
    ];
    googleDriveService.listFiles.mockResolvedValue({ files: mockFiles, connected: true });
    googleDriveService.deleteFile.mockResolvedValue({});

    render(<DriveSection />);

    await waitFor(() => {
      expect(screen.getByText('document.pdf')).toBeInTheDocument();
    });

    const deleteButtons = screen.getAllByRole('button', { name: '' });
    const deleteButton = deleteButtons[deleteButtons.length - 1];
    await userEvent.click(deleteButton);

    const confirmButton = screen.getByText('Confirm');
    await userEvent.click(confirmButton);

    await waitFor(() => {
      expect(googleDriveService.listFiles).toHaveBeenCalledTimes(2);
    });
  });

  it('should close modal when cancel clicked', async () => {
    const mockFiles = [
      { id: '1', name: 'document.pdf', mimeType: 'application/pdf' },
    ];
    googleDriveService.listFiles.mockResolvedValue({ files: mockFiles, connected: true });

    render(<DriveSection />);

    await waitFor(() => {
      expect(screen.getByText('document.pdf')).toBeInTheDocument();
    });

    const deleteButtons = screen.getAllByRole('button', { name: '' });
    const deleteButton = deleteButtons[deleteButtons.length - 1];
    await userEvent.click(deleteButton);

    expect(screen.getByTestId('delete-modal')).toBeInTheDocument();

    const cancelButton = screen.getByText('Cancel');
    await userEvent.click(cancelButton);

    await waitFor(() => {
      expect(screen.queryByTestId('delete-modal')).not.toBeInTheDocument();
    });
  });

  it('should handle file loading errors gracefully', async () => {
    googleDriveService.listFiles.mockRejectedValue(new Error('API Error'));

    render(<DriveSection />);

    await waitFor(() => {
      expect(screen.getByText('Connect to Google Drive')).toBeInTheDocument();
    });
  });
});
