import { expect, type Page } from "@playwright/test";

export class ProfilePage {
  private readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async deleteUser(password: string) {
    await this.page.getByRole('link', { name: 'Deletar Conta' }).click();
    await this.page.getByRole('textbox', { name: 'Confirme sua senha:' }).fill(password);
    await this.page.getByRole('button', { name: 'Excluir' }).click();
  }
}