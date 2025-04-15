import { test } from "../fixtures/fixtures"

test("should go to home page", async ({ homePage }) => {
  await homePage.goto();
});