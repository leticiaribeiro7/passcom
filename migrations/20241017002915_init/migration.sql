-- CreateTable
CREATE TABLE "Trecho" (
    "id" SERIAL NOT NULL,
    "origem" TEXT NOT NULL,
    "destino" TEXT NOT NULL,

    CONSTRAINT "Trecho_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Assento" (
    "id" SERIAL NOT NULL,
    "numero" INTEGER NOT NULL,
    "id_trecho" INTEGER NOT NULL,

    CONSTRAINT "Assento_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "TrechoReservado" (
    "id" SERIAL NOT NULL,
    "uuid_passagem" TEXT NOT NULL,
    "id_trecho" INTEGER NOT NULL,
    "id_assento" INTEGER NOT NULL,

    CONSTRAINT "TrechoReservado_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Passagem" (
    "uuid" TEXT NOT NULL,
    "user_id" INTEGER NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Passagem_pkey" PRIMARY KEY ("uuid")
);

-- CreateTable
CREATE TABLE "User" (
    "id" SERIAL NOT NULL,
    "login" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_login_key" ON "User"("login");

-- AddForeignKey
ALTER TABLE "Assento" ADD CONSTRAINT "Assento_id_trecho_fkey" FOREIGN KEY ("id_trecho") REFERENCES "Trecho"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TrechoReservado" ADD CONSTRAINT "TrechoReservado_uuid_passagem_fkey" FOREIGN KEY ("uuid_passagem") REFERENCES "Passagem"("uuid") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TrechoReservado" ADD CONSTRAINT "TrechoReservado_id_trecho_fkey" FOREIGN KEY ("id_trecho") REFERENCES "Trecho"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TrechoReservado" ADD CONSTRAINT "TrechoReservado_id_assento_fkey" FOREIGN KEY ("id_assento") REFERENCES "Assento"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Passagem" ADD CONSTRAINT "Passagem_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
