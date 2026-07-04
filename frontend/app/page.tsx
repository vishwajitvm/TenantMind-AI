'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useStore } from '../components/store';

export default function Home() {
  const router = useRouter();
  const isAuthenticated = useStore(state => state.isAuthenticated);

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/org-selector');
    } else {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="animate-pulse text-indigo-400 font-mono text-sm">
        Authenticating Keycloak gateway parameters...
      </div>
    </div>
  );
}
