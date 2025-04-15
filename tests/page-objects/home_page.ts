import { expect, type Locator, type Page } from '@playwright/test';
import dotenv from 'dotenv';
dotenv.config();

const URL = 'http://127.0.0.1:' + process.env.AVAILABLE_PORT;

export class HomePage {
  private readonly page: Page;

  constructor (page: Page) {
    this.page = page;
  }

  async goto() {
    await this.page.goto(URL);
  }
}