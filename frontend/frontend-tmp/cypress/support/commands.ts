/// <reference types="cypress" />

declare global {
  namespace Cypress {
    interface Chainable {
      login(username: string, password: string): Chainable<void>;
      calculateKundli(data: {
        date: string;
        time: string;
        latitude: number;
        longitude: number;
        timezone: string;
      }): Chainable<void>;
    }
  }
}

Cypress.Commands.add('login', (username: string, password: string) => {
  cy.visit('/login');
  cy.get('[data-testid="username-input"]').type(username);
  cy.get('[data-testid="password-input"]').type(password);
  cy.get('[data-testid="login-submit"]').click();
  cy.url().should('eq', Cypress.config().baseUrl + '/');
});

Cypress.Commands.add('calculateKundli', (data) => {
  cy.visit('/calculate');
  cy.get('[data-testid="date-input"]').type(data.date);
  cy.get('[data-testid="time-input"]').type(data.time);
  cy.get('[data-testid="latitude-input"]').type(data.latitude.toString());
  cy.get('[data-testid="longitude-input"]').type(data.longitude.toString());
  cy.get('[data-testid="timezone-input"]').select(data.timezone);
  cy.get('[data-testid="calculate-submit"]').click();
  cy.get('[data-testid="kundli-chart"]').should('exist');
});

export {};
