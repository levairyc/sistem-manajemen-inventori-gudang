import streamlit as st

from database import Base, engine, SessionLocal
from models import Barang, Gudang, StokGudang


# ============================================================
# DATABASE
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# JUDUL
# ============================================================

st.title("Sistem Manajemen Inventori Gudang")
st.write("Aplikasi pengelolaan barang dan stok gudang.")


# ============================================================
# MENU
# ============================================================

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Kelola Data Barang",
        "Kelola Data Gudang",
        "Penerimaan Barang",
        "Barang Keluar",
        "Kelola Stok",
        "Transfer Antar Gudang",
        "Cek Stok",
        "Peringatan Stok",
        "Laporan"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if menu == "Dashboard":

    st.subheader("Dashboard")

    db = SessionLocal()

    jumlah_barang = db.query(Barang).count()
    jumlah_gudang = db.query(Gudang).count()

    db.close()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Jumlah Jenis Barang", jumlah_barang)

    with col2:
        st.metric("Jumlah Gudang", jumlah_gudang)


# ============================================================
# KELOLA DATA BARANG
# ============================================================

elif menu == "Kelola Data Barang":

    st.subheader("Kelola Data Barang")

    nama_barang = st.text_input("Nama Barang")
    kategori = st.text_input("Kategori")

    stok_minimum = st.number_input(
        "Stok Minimum",
        min_value=0,
        step=1
    )

    if st.button("Simpan Barang"):

        if nama_barang.strip() == "":
            st.error("Nama barang harus diisi.")

        elif kategori.strip() == "":
            st.error("Kategori harus diisi.")

        else:

            db = SessionLocal()

            barang = Barang(
                nama_barang=nama_barang,
                kategori=kategori,
                stok=0,
                stok_minimum=stok_minimum
            )

            db.add(barang)
            db.commit()
            db.close()

            st.success("Data barang berhasil disimpan.")


# ============================================================
# KELOLA DATA GUDANG
# ============================================================

elif menu == "Kelola Data Gudang":

    st.subheader("Kelola Data Gudang")

    # -------------------------
    # FORM TAMBAH GUDANG
    # -------------------------

    nama_gudang = st.text_input("Nama Gudang")
    lokasi = st.text_input("Lokasi")

    if st.button("Simpan Gudang"):

        if nama_gudang.strip() == "":
            st.error("Nama gudang harus diisi.")

        elif lokasi.strip() == "":
            st.error("Lokasi harus diisi.")

        else:

            db = SessionLocal()

            gudang = Gudang(
                nama_gudang=nama_gudang,
                lokasi=lokasi
            )

            db.add(gudang)
            db.commit()
            db.close()

            st.success("Data gudang berhasil disimpan.")

            st.rerun()

    # -------------------------
    # DAFTAR GUDANG
    # -------------------------

    st.divider()

    st.subheader("Daftar Gudang")

    db = SessionLocal()

    gudang_list = db.query(
        Gudang
    ).order_by(
        Gudang.id_gudang
    ).all()

    if gudang_list:

        data_gudang = []

        for gudang in gudang_list:

            data_gudang.append({
                "ID Gudang": gudang.id_gudang,
                "Nama Gudang": gudang.nama_gudang,
                "Lokasi": gudang.lokasi
            })

        st.dataframe(
            data_gudang,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Belum ada data gudang.")

    db.close()


# ============================================================
# PENERIMAAN BARANG
# ============================================================

elif menu == "Penerimaan Barang":

    st.subheader("Penerimaan Barang")

    db = SessionLocal()

    barang_list = db.query(Barang).all()
    gudang_list = db.query(Gudang).all()

    if not barang_list:

        st.warning("Belum ada data barang.")
        db.close()

    elif not gudang_list:

        st.warning("Belum ada data gudang.")
        db.close()

    else:

        barang_options = {
            f"{barang.id_barang} - {barang.nama_barang}":
            barang.id_barang
            for barang in barang_list
        }

        gudang_options = {
            f"{gudang.id_gudang} - {gudang.nama_gudang}":
            gudang.id_gudang
            for gudang in gudang_list
        }

        barang_pilihan = st.selectbox(
            "Pilih Barang",
            list(barang_options.keys())
        )

        gudang_pilihan = st.selectbox(
            "Pilih Gudang",
            list(gudang_options.keys())
        )

        jumlah = st.number_input(
            "Jumlah Barang",
            min_value=1,
            step=1
        )

        if st.button("Terima Barang"):

            id_barang = barang_options[barang_pilihan]
            id_gudang = gudang_options[gudang_pilihan]

            barang = db.query(Barang).filter(
                Barang.id_barang == id_barang
            ).first()

            stok_gudang = db.query(
                StokGudang
            ).filter(
                StokGudang.id_barang == id_barang,
                StokGudang.id_gudang == id_gudang
            ).first()

            if stok_gudang:

                stok_gudang.stok += jumlah

            else:

                stok_gudang = StokGudang(
                    id_barang=id_barang,
                    id_gudang=id_gudang,
                    stok=jumlah
                )

                db.add(stok_gudang)

            barang.tambah_stok(jumlah)

            db.commit()
            db.close()

            st.success(
                f"Barang berhasil diterima. "
                f"Stok bertambah {jumlah}."
            )


# ============================================================
# BARANG KELUAR
# ============================================================

elif menu == "Barang Keluar":

    st.subheader("Mencatat Barang Keluar")

    db = SessionLocal()

    barang_list = db.query(Barang).all()
    gudang_list = db.query(Gudang).all()

    if not barang_list:

        st.warning("Belum ada data barang.")
        db.close()

    elif not gudang_list:

        st.warning("Belum ada data gudang.")
        db.close()

    else:

        barang_options = {
            f"{barang.id_barang} - {barang.nama_barang}":
            barang.id_barang
            for barang in barang_list
        }

        gudang_options = {
            f"{gudang.id_gudang} - {gudang.nama_gudang}":
            gudang.id_gudang
            for gudang in gudang_list
        }

        barang_pilihan = st.selectbox(
            "Pilih Barang",
            list(barang_options.keys())
        )

        gudang_pilihan = st.selectbox(
            "Pilih Gudang",
            list(gudang_options.keys())
        )

        jumlah = st.number_input(
            "Jumlah Barang",
            min_value=1,
            step=1
        )

        if st.button("Keluarkan Barang"):

            id_barang = barang_options[barang_pilihan]
            id_gudang = gudang_options[gudang_pilihan]

            barang = db.query(Barang).filter(
                Barang.id_barang == id_barang
            ).first()

            stok_gudang = db.query(
                StokGudang
            ).filter(
                StokGudang.id_barang == id_barang,
                StokGudang.id_gudang == id_gudang
            ).first()

            if not stok_gudang:

                st.error(
                    "Stok barang di gudang tersebut belum tersedia."
                )

            elif jumlah > stok_gudang.stok:

                st.error(
                    "Stok di gudang tidak mencukupi."
                )

            else:

                stok_gudang.stok -= jumlah
                barang.kurangi_stok(jumlah)

                db.commit()

                st.success(
                    f"Barang berhasil dikeluarkan. "
                    f"Stok berkurang {jumlah}."
                )

            db.close()


# ============================================================
# KELOLA STOK
# ============================================================

elif menu == "Kelola Stok":

    st.subheader("Kelola Stok Barang di Gudang")

    db = SessionLocal()

    barang_list = db.query(Barang).all()
    gudang_list = db.query(Gudang).all()

    if not barang_list:

        st.warning("Belum ada data barang.")
        db.close()

    elif not gudang_list:

        st.warning("Belum ada data gudang.")
        db.close()

    else:

        barang_options = {
            f"{barang.id_barang} - {barang.nama_barang}":
            barang.id_barang
            for barang in barang_list
        }

        gudang_options = {
            f"{gudang.id_gudang} - {gudang.nama_gudang}":
            gudang.id_gudang
            for gudang in gudang_list
        }

        barang_pilihan = st.selectbox(
            "Pilih Barang",
            list(barang_options.keys())
        )

        gudang_pilihan = st.selectbox(
            "Pilih Gudang",
            list(gudang_options.keys())
        )

        stok = st.number_input(
            "Jumlah Stok",
            min_value=0,
            step=1
        )

        if st.button("Simpan Stok"):

            id_barang = barang_options[barang_pilihan]
            id_gudang = gudang_options[gudang_pilihan]

            barang = db.query(Barang).filter(
                Barang.id_barang == id_barang
            ).first()

            stok_gudang = db.query(
                StokGudang
            ).filter(
                StokGudang.id_barang == id_barang,
                StokGudang.id_gudang == id_gudang
            ).first()

            if stok_gudang:

                perubahan = stok - stok_gudang.stok
                stok_gudang.stok = stok
                barang.stok += perubahan

            else:

                stok_gudang = StokGudang(
                    id_barang=id_barang,
                    id_gudang=id_gudang,
                    stok=stok
                )

                db.add(stok_gudang)
                barang.stok += stok

            db.commit()
            db.close()

            st.success("Stok berhasil disimpan.")


# ============================================================
# TRANSFER ANTAR GUDANG
# ============================================================

elif menu == "Transfer Antar Gudang":

    st.subheader("Transfer Antar Gudang")

    db = SessionLocal()

    barang_list = db.query(Barang).all()
    gudang_list = db.query(Gudang).order_by(
        Gudang.id_gudang
    ).all()

    # Tampilkan jumlah gudang
    st.info(
        f"Jumlah gudang yang tersedia: {len(gudang_list)}"
    )

    if not barang_list:

        st.warning("Belum ada data barang.")

    elif len(gudang_list) < 2:

        st.warning(
            "Minimal harus ada 2 gudang untuk melakukan transfer."
        )

        st.write("Gudang yang terdaftar:")

        for gudang in gudang_list:

            st.write(
                f"- ID {gudang.id_gudang}: "
                f"{gudang.nama_gudang} - "
                f"{gudang.lokasi}"
            )

    else:

        barang_options = {
            f"{barang.id_barang} - {barang.nama_barang}":
            barang.id_barang
            for barang in barang_list
        }

        gudang_options = {
            f"{gudang.id_gudang} - {gudang.nama_gudang}":
            gudang.id_gudang
            for gudang in gudang_list
        }

        barang_pilihan = st.selectbox(
            "Pilih Barang",
            list(barang_options.keys())
        )

        gudang_asal_pilihan = st.selectbox(
            "Pilih Gudang Asal",
            list(gudang_options.keys())
        )

        gudang_tujuan_pilihan = st.selectbox(
            "Pilih Gudang Tujuan",
            list(gudang_options.keys())
        )

        jumlah = st.number_input(
            "Jumlah Transfer",
            min_value=1,
            step=1
        )

        if st.button("Transfer Barang"):

            id_barang = barang_options[barang_pilihan]

            id_gudang_asal = gudang_options[
                gudang_asal_pilihan
            ]

            id_gudang_tujuan = gudang_options[
                gudang_tujuan_pilihan
            ]

            if id_gudang_asal == id_gudang_tujuan:

                st.error(
                    "Gudang asal dan tujuan harus berbeda."
                )

            else:

                stok_asal = db.query(
                    StokGudang
                ).filter(
                    StokGudang.id_barang == id_barang,
                    StokGudang.id_gudang == id_gudang_asal
                ).first()

                stok_tujuan = db.query(
                    StokGudang
                ).filter(
                    StokGudang.id_barang == id_barang,
                    StokGudang.id_gudang == id_gudang_tujuan
                ).first()

                if not stok_asal:

                    st.error(
                        "Stok barang di gudang asal belum tersedia."
                    )

                elif jumlah > stok_asal.stok:

                    st.error(
                        "Stok di gudang asal tidak mencukupi."
                    )

                else:

                    stok_asal.stok -= jumlah

                    if stok_tujuan:

                        stok_tujuan.stok += jumlah

                    else:

                        stok_tujuan = StokGudang(
                            id_barang=id_barang,
                            id_gudang=id_gudang_tujuan,
                            stok=jumlah
                        )

                        db.add(stok_tujuan)

                    db.commit()

                    st.success(
                        f"Transfer {jumlah} barang berhasil."
                    )

    db.close()


# ============================================================
# CEK STOK
# ============================================================

elif menu == "Cek Stok":

    st.subheader("Mengecek Stok Barang")

    db = SessionLocal()

    barang_list = db.query(Barang).all()
    gudang_list = db.query(Gudang).all()

    if not barang_list:

        st.warning("Belum ada data barang.")

    elif not gudang_list:

        st.warning("Belum ada data gudang.")

    else:

        barang_options = {
            f"{barang.id_barang} - {barang.nama_barang}":
            barang.id_barang
            for barang in barang_list
        }

        gudang_options = {
            f"{gudang.id_gudang} - {gudang.nama_gudang}":
            gudang.id_gudang
            for gudang in gudang_list
        }

        barang_pilihan = st.selectbox(
            "Pilih Barang",
            list(barang_options.keys())
        )

        gudang_pilihan = st.selectbox(
            "Pilih Gudang",
            list(gudang_options.keys())
        )

        if st.button("Cek Stok"):

            id_barang = barang_options[barang_pilihan]
            id_gudang = gudang_options[gudang_pilihan]

            stok_gudang = db.query(
                StokGudang
            ).filter(
                StokGudang.id_barang == id_barang,
                StokGudang.id_gudang == id_gudang
            ).first()

            if stok_gudang:

                st.success(
                    f"Stok barang: {stok_gudang.stok}"
                )

            else:

                st.info(
                    "Belum ada stok barang di gudang tersebut."
                )

    db.close()


# ============================================================
# PERINGATAN STOK
# ============================================================

elif menu == "Peringatan Stok":

    st.subheader("Melihat Peringatan Stok")

    db = SessionLocal()

    barang_list = db.query(Barang).all()

    if not barang_list:

        st.info("Belum ada data barang.")

    else:

        ada_peringatan = False

        for barang in barang_list:

            if barang.cek_peringatan_stok():

                st.warning(
                    f"{barang.nama_barang} | "
                    f"Stok total: {barang.stok} | "
                    f"Minimum: {barang.stok_minimum}"
                )

                ada_peringatan = True

        if not ada_peringatan:

            st.success(
                "Tidak ada barang dengan stok di bawah batas minimum."
            )

    db.close()


# ============================================================
# LAPORAN
# ============================================================

elif menu == "Laporan":

    st.subheader("Laporan Inventori")

    db = SessionLocal()

    barang_list = db.query(Barang).all()

    if not barang_list:

        st.info("Belum ada data barang.")

    else:

        data_laporan = []

        for barang in barang_list:

            data_laporan.append({
                "ID Barang": barang.id_barang,
                "Nama Barang": barang.nama_barang,
                "Kategori": barang.kategori,
                "Stok Total": barang.stok,
                "Stok Minimum": barang.stok_minimum
            })

        st.dataframe(
            data_laporan,
            use_container_width=True,
            hide_index=True
        )

    db.close()