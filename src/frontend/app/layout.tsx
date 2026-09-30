import "./globals.css";
import Link from "next/link";
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body>
    <div className="top">
      <Link href="/status"><strong>Failover Pulse</strong></Link>
      <Link href="/status">Status</Link>
      <Link href="/board">Board</Link>
      <Link href="/login">Account</Link>
    </div>{children}
  </body></html>);
}
