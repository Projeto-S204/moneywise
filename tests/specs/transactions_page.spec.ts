import { test } from "../fixtures/fixtures"

test.beforeEach(async ({ baseSetup, homePage, signupPage, signinPage }) => {
  await baseSetup.goto();
  await homePage.gotoSignupPage();
  await signupPage.register('test', 'test@test.com', '!Test12345678', '!Test12345678', '2002-09-29');
  await signinPage.login('test@test.com', '!Test12345678');
});

test.afterEach(async ({ signinPage, transactionsPage, profilePage }) => {
  await transactionsPage.gotoProfilePage();
  await profilePage.deleteUser('!Test12345678');
});

test("should be able to create a transaction", async ({ transactionsPage }) => {
  const transactionData = {
    title: "Transaction",
    paymentMethod: "PIX",
    value: "100.00",
    date: "2023-10-01",
    category: "Casa",
    description: "Test Description",
    is_recurring: true,
    installments: "5",
    type: "Despesa"
  };

  await transactionsPage.fillTransactionFields(transactionData);
  await transactionsPage.expectTransactionToBeViewed(transactionData);
});

test("should be able to update a transaction", async ({ transactionsPage }) => {
  const updatedTransactionData = {
    title: "Updated Transaction",
    paymentMethod: "Credito",
    value: "150.00",
    date: "2023-10-02",
    category: "Entretenimento",
    description: "Updated Description",
    is_recurring: true,
    installments: "3",
    type: "Receita"
  };

  await transactionsPage.fillTransactionFields(updatedTransactionData);
  await transactionsPage.expectTransactionToBeViewed(updatedTransactionData);
});

test("should be able to delete a transaction", async ({ transactionsPage }) => {
  const transactionData = {
    title: "Transaction to Delete",
    paymentMethod: "PIX",
    value: "100.00",
    date: "2023-10-01",
    category: "Casa",
    description: "Test Description",
    is_recurring: false,
    type: "Despesa"
  };

  await transactionsPage.fillTransactionFields(transactionData);
  await transactionsPage.viewTransaction(transactionData.title);
  await transactionsPage.deleteTransaction(transactionData.title);
  await transactionsPage.expectTransactionNotToExist(transactionData.title);
});
