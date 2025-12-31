import './globals.css';

export const metadata = {
  title: 'FlowTask - Streamlined Task Management',
  description: 'Organize your workflow with our intuitive task management solution',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased bg-gradient-to-br from-gray-900 via-indigo-900/20 to-black">
        {children}
      </body>
    </html>
  );
}