describe('Authentication Flow', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('should navigate to login page', () => {
    cy.get('[data-testid="login-button"]').click();
    cy.url().should('include', '/login');
  });

  it('should show validation errors on empty form submission', () => {
    cy.visit('/login');
    cy.get('[data-testid="login-submit"]').click();
    cy.contains('Username is required');
    cy.contains('Password is required');
  });

  it('should login successfully with valid credentials', () => {
    cy.visit('/login');
    cy.get('[data-testid="username-input"]').type('testuser');
    cy.get('[data-testid="password-input"]').type('password123');
    cy.get('[data-testid="login-submit"]').click();
    cy.url().should('eq', Cypress.config().baseUrl + '/');
    cy.get('[data-testid="user-menu"]').should('exist');
  });

  it('should show error message with invalid credentials', () => {
    cy.visit('/login');
    cy.get('[data-testid="username-input"]').type('wronguser');
    cy.get('[data-testid="password-input"]').type('wrongpass');
    cy.get('[data-testid="login-submit"]').click();
    cy.contains('Invalid username or password');
  });

  it('should logout successfully', () => {
    // Login first
    cy.login('testuser', 'password123');
    
    // Then logout
    cy.get('[data-testid="user-menu"]').click();
    cy.get('[data-testid="logout-button"]').click();
    
    // Verify logged out state
    cy.get('[data-testid="login-button"]').should('exist');
    cy.get('[data-testid="user-menu"]').should('not.exist');
  });
});
