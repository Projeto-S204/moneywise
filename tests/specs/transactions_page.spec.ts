import { test } from "../fixtures/fixtures"

test.beforeEach(async ({ baseSetup, homePage, signinPage }) => {
  await baseSetup.goto();
  await homePage.gotoSigninPage();
  await signinPage.login('teste@teste.com', '12345678');
});

test("should be able to create a transaction", async ({ baseSetup, transactionsPage }) => {
  const transactionData = {
    title: "Test Transaction",
    paymentMethod: "PIX",
    value: "100.00",
    date: "2023-10-01",
    category: "Casa",
    description: "Test Description",
    installments: "5",
    type: "Despesa"
  };

  await transactionsPage.createTransaction(transactionData);
  await transactionsPage.expectTransactionToBeCreated(transactionData);
});

test.describe("Tests that need to create a transaction first", () => {
  test.beforeEach(async ({ transactionsPage }) => {
    const transactionData = {
      title: "Test Transaction",
      paymentMethod: "PIX",
      value: "100.00",
      date: "2023-10-01",
      category: "Casa",
      description: "Test Description",
      installments: "5",
      type: "Despesa"
    };

    await transactionsPage.createTransaction(transactionData);
  });

  test("should be able to read a transaction", async ({ baseSetup, transactionsPage }) => {
    
  });

  test("should be able to update a transaction", async ({ baseSetup, transactionsPage }) => {
  });

  test("should be able to delete a transaction", async ({ baseSetup, transactionsPage }) => {
  });
});