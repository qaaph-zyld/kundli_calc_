import React from 'react';
import { Box, AppBar, Toolbar, IconButton, Typography, useTheme } from '@mui/material';
import { Menu as MenuIcon } from '@mui/icons-material';
import { AccessibilityMenu } from '../common/AccessibilityMenu';
import { useAuth } from '../../contexts/AuthContext';
import UserMenu from './UserMenu';
import Sidebar from './Sidebar';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = React.useState(false);
  const theme = useTheme();
  const { isAuthenticated } = useAuth();

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <AppBar
        position="fixed"
        sx={{
          zIndex: theme.zIndex.drawer + 1,
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open menu"
            edge="start"
            onClick={toggleSidebar}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            component="h1"
            sx={{ flexGrow: 1 }}
            role="heading"
            aria-level={1}
          >
            Kundli App
          </Typography>
          <AccessibilityMenu />
          {isAuthenticated && <UserMenu />}
        </Toolbar>
      </AppBar>
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${240}px)` },
          mt: '64px',
        }}
        role="main"
      >
        {children}
      </Box>
    </Box>
  );
};

export default Layout;
