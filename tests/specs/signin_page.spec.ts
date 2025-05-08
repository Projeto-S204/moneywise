import { test } from "../fixtures/fixtures"

test.beforeEach(async ({ homePage }) => {
  await homePage.gotoSigninPage();
});

test.describe("Login Methods", () => {
  test("should be able to login with valid credentials", async ({ baseSetup, signinPage }) => {
    await signinPage.login('test@test.com', '!Test12345678');
    await baseSetup.expectURL('/transactions/');
  });

  test("should not be able to login with invalid credentials", async ({ signinPage }) => {
    await signinPage.login('invalidEmail', 'invalidPassword');
    await signinPage.expectError();
  });
});