/*
  Warnings:

  - You are about to drop the column `portfolioId` on the `Asset` table. All the data in the column will be lost.
  - You are about to drop the column `portfolioId` on the `Transaction` table. All the data in the column will be lost.
  - You are about to drop the `Portfolio` table. If the table is not empty, all the data it contains will be lost.
  - A unique constraint covering the columns `[symbol]` on the table `Asset` will be added. If there are existing duplicate values, this will fail.

*/
-- DropForeignKey
ALTER TABLE "Asset" DROP CONSTRAINT "Asset_portfolioId_fkey";

-- DropForeignKey
ALTER TABLE "Transaction" DROP CONSTRAINT "Transaction_portfolioId_fkey";

-- AlterTable
ALTER TABLE "Asset" DROP COLUMN "portfolioId";

-- AlterTable
ALTER TABLE "Transaction" DROP COLUMN "portfolioId";

-- DropTable
DROP TABLE "Portfolio";

-- CreateIndex
CREATE UNIQUE INDEX "Asset_symbol_key" ON "Asset"("symbol");
