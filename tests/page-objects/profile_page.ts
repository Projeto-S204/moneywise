import type { Page } from "@playwright/test";

export class ProfilePage {
  private readonly page: Page;
  
  constructor(page: Page) {
    this.page = page;
  }
}