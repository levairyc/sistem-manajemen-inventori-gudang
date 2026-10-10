from database import Base, engine


def main():
    Base.metadata.create_all(bind=engine)

    print("==========================================")
    print(" SISTEM MANAJEMEN INVENTORI GUDANG")
    print("==========================================")
    print("Database berhasil disiapkan.")
    print()
    print("Menu utama digunakan melalui aplikasi Streamlit.")


if __name__ == "__main__":
    main()