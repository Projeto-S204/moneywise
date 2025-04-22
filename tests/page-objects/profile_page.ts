import { expect, type Page } from "@playwright/test";

export class ProfilePage {
  private readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async deleteUser() {
    this.page.once('dialog', async (dialog) => {
      expect(dialog.type()).toBe('confirm');
      expect(dialog.message()).toContain('Tem certeza que deseja deletar sua conta? Esta ação é irreversível!');
      await dialog.accept();
    });

    this.page.once('dialog', async (dialog) => {
      expect(dialog.type()).toBe('alert');
      expect(dialog.message()).toContain('Conta deletada com sucesso!');
      await dialog.accept();
    });

    await this.page.getByRole('link', { name: 'Deletar Conta' }).click();
  }
}