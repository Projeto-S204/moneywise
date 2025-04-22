import { test } from "../fixtures/fixtures"

test.describe("Registration Methods", () => {
  // test.afterEach(async ({ signinPage, transactionsPage, profilePage }) => {
  //   await signinPage.login('test@test.com', '12345678');
  //   await transactionsPage.gotoProfilePage();
  //   await profilePage.deleteUser();
  // });

  test("should be able to register with valid credentials", async ({ baseSetup, signupPage }) => {
    await signupPage.register('test', 'test@test.com', '12345678', '12345678', '2002-09-29');
    await baseSetup.expectURL('/signin');
  });

});

test("should not be able to register with invalid email", async ({ signupPage }) => {
  await signupPage.register('test', 'Invalid Email', '12345678', '12345678', '2002-09-29');
  await signupPage.emailError();
});

test("should not be able to register with different passwords", async ({ signupPage }) => {
  await signupPage.register('test', 'Invalid Email', '12345678', 'different pass', '2002-09-29');
  await signupPage.passwordError();
});