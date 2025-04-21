import { expect, type Page } from "@playwright/test";

export class BaseSetup {
  private readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  getPage() {
    return this.page;
  }

  async goto(url: string) {
    await this.page.goto(url);
  }

  async expectURL(currentPage: string) {
    const CURRENT_URL = await this.page.url();
    expect(CURRENT_URL).toContain(currentPage);
  }

}
