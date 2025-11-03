"use client";
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../contexts/AuthContext';
import AuthModal from './AuthModal';
import styles from './Header.module.css';

export default function Header() {
  const router = useRouter();
  const { user, signOut, loading } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'signup'>('login');
  const [showUserMenu, setShowUserMenu] = useState(false);

  const handleAuthClick = (mode: 'login' | 'signup') => {
    setAuthMode(mode);
    setShowAuthModal(true);
  };

  const handleSignOut = async () => {
    await signOut();
    setShowUserMenu(false);
  };

  if (loading) {
    return (
      <header className={styles.header}>
        <div className={styles.container}>
          <h1>Kundli Calculator</h1>
          <div className={styles.loading}>Loading...</div>
        </div>
      </header>
    );
  }

  return (
    <>
      <header className={styles.header}>
        <div className={styles.container}>
          <div className={styles.logo}>
            <h1>Kundli Calculator</h1>
            <p>Vedic Astrology Chart Generator</p>
          </div>

          <nav className={styles.nav}>
            {user ? (
              <div className={styles.userSection}>
                <button 
                  className={styles.userButton}
                  onClick={() => setShowUserMenu(!showUserMenu)}
                >
                  <span className={styles.userIcon}>👤</span>
                  <span className={styles.userName}>
                    {user.user_metadata?.full_name || user.email}
                  </span>
                  <span className={styles.dropdownIcon}>▼</span>
                </button>

                {showUserMenu && (
                  <div className={styles.userMenu}>
                    <div className={styles.userInfo}>
                      <div className={styles.userEmail}>{user.email}</div>
                    </div>
                    <button 
                      onClick={() => { 
                        router.push('/my-charts'); 
                        setShowUserMenu(false);
                      }} 
                      className={styles.menuItem}
                    >
                      📊 My Charts
                    </button>
                    <button onClick={handleSignOut} className={styles.menuItem}>
                      🚪 Sign Out
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div className={styles.authButtons}>
                <button 
                  onClick={() => handleAuthClick('login')}
                  className={styles.loginBtn}
                >
                  Login
                </button>
                <button 
                  onClick={() => handleAuthClick('signup')}
                  className={styles.signupBtn}
                >
                  Sign Up
                </button>
              </div>
            )}
          </nav>
        </div>
      </header>

      <AuthModal 
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        defaultMode={authMode}
      />
    </>
  );
}
