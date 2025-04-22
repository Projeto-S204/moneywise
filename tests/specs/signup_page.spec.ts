import { test } from "../fixtures/fixtures"

test.describe("Registration Methods", () => {
  test.afterEach(async ({ signupPage, transactionsPage, profilePage }) => {
    await signupPage.returnToSignupPage();
  });

  test("should be able to register with valid credentials", async ({ baseSetup, signupPage }) => {
    await signupPage.register('autotest', 'auto@auto.com', '12345678', '12345678', '2002-09-29');
    await baseSetup.expectURL('/signin');
  });

});

test("should not be able to register with invalid email", async ({ signupPage }) => {
  await signupPage.register('autotest', 'Invalid Email', '12345678', '12345678', '2002-09-29');
  await signupPage.emailError();
});

test("should not be able to register with different passwords", async ({ signupPage }) => {
  await signupPage.register('autotest', 'Invalid Email', '12345678', 'different pass', '2002-09-29');
  await signupPage.passwordError();
});