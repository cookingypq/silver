import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App.jsx';

describe('App', () => {
  it('renders input and analyze button', () => {
    render(<App />);
    expect(screen.getByLabelText(/RustSec/i)).toBeInTheDocument();
    expect(screen.getByText(/Analyze/i)).toBeInTheDocument();
  });

  it('can input RustSec IDs and trigger analysis', async () => {
    render(<App />);
    const textarea = screen.getByLabelText(/RustSec/i);
    fireEvent.change(textarea, { target: { value: 'RUSTSEC-2022-0001' } });
    const button = screen.getByText(/Analyze/i);
    fireEvent.click(button);
    expect(button).toBeDisabled();
    await waitFor(() => expect(screen.getByText(/Analyzing/i)).toBeInTheDocument());
    await waitFor(() => expect(screen.getByText(/Analyzed|Failed/i)).toBeInTheDocument(), { timeout: 2000 });
  });
}); 