
import streamlit as st
import pandas as pd

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 Ứng dụng tính lãi tiết kiệm")
st.write("Tính toán tiền lãi theo **lãi đơn** hoặc **lãi kép**.")

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================

so_tien = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "📅 Kỳ hạn",
    min_value=1,
    value=12,
    step=1
)

don_vi_ky_han = st.selectbox(
    "Đơn vị kỳ hạn",
    ["Tháng", "Năm"]
)

lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

hinh_thuc_lai = st.selectbox(
    "🧮 Hình thức tính lãi",
    ["Lãi đơn", "Lãi kép"]
)

hinh_thuc_nhan = st.selectbox(
    "💳 Hình thức nhận lãi",
    ["Lãnh lãi hàng tháng", "Lãnh lãi hàng quý", "Lãnh lãi cuối kỳ"]
)

st.divider()

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================

def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# =========================
# TÍNH TOÁN
# =========================

if st.button("🔍 TÍNH TIỀN LÃI", use_container_width=True):

    # Chuyển kỳ hạn về số tháng
    if don_vi_ky_han == "Năm":
        tong_thang = ky_han * 12
    else:
        tong_thang = ky_han

    # Lãi suất tháng
    lai_suat_nam = lai_suat / 100
    lai_suat_thang = lai_suat_nam / 12

    # Xác định số kỳ nhận lãi
    if hinh_thuc_nhan == "Lãnh lãi hàng tháng":
        so_ky = tong_thang
        so_thang_moi_ky = 1

    elif hinh_thuc_nhan == "Lãnh lãi hàng quý":
        so_ky = tong_thang // 3
        so_thang_moi_ky = 3

    else:
        so_ky = 1
        so_thang_moi_ky = tong_thang

    # =========================
    # LÃI ĐƠN
    # =========================
    if hinh_thuc_lai == "Lãi đơn":

        # Tổng lãi
        tong_lai = so_tien * lai_suat_nam * (tong_thang / 12)

        # Tiền lãi mỗi kỳ
        lai_moi_ky = so_tien * lai_suat_thang * so_thang_moi_ky

        # Tạo bảng
        du_lieu = []

        for i in range(1, int(so_ky) + 1):
            du_lieu.append({
                "Kỳ": i,
                "Số tiền gốc": dinh_dang_tien(so_tien),
                "Tiền lãi kỳ này": dinh_dang_tien(lai_moi_ky),
                "Tổng lãi tích lũy": dinh_dang_tien(lai_moi_ky * i)
            })

        tong_tien = so_tien + tong_lai

    # =========================
    # LÃI KÉP
    # =========================
    else:

        # Lãi kép được nhập lại vào vốn theo kỳ nhận lãi
        lai_suat_ky = lai_suat_nam * (so_thang_moi_ky / 12)

        von_hien_tai = so_tien
        tong_lai = 0

        du_lieu = []

        for i in range(1, int(so_ky) + 1):

            lai_ky = von_hien_tai * lai_suat_ky

            tong_lai += lai_ky
            von_hien_tai += lai_ky

            du_lieu.append({
                "Kỳ": i,
                "Số tiền đầu kỳ": dinh_dang_tien(von_hien_tai - lai_ky),
                "Tiền lãi kỳ này": dinh_dang_tien(lai_ky),
                "Số tiền cuối kỳ": dinh_dang_tien(von_hien_tai)
            })

        tong_tien = von_hien_tai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================

    st.success("✅ Đã tính toán thành công!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 Tiền lãi định kỳ",
            dinh_dang_tien(lai_moi_ky)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            dinh_dang_tien(tong_lai)
        )

    with col3:
        st.metric(
            "💵 Tổng gốc + lãi",
            dinh_dang_tien(tong_tien)
        )

    st.divider()

    # =========================
    # THÔNG TIN GỬI
    # =========================

    st.subheader("📋 Thông tin khoản tiền gửi")

    thong_tin = pd.DataFrame({
        "Thông tin": [
            "Số tiền gửi",
            "Kỳ hạn",
            "Lãi suất",
            "Hình thức tính lãi",
            "Hình thức nhận lãi"
        ],
        "Giá trị": [
            dinh_dang_tien(so_tien),
            f"{ky_han} {don_vi_ky_han}",
            f"{lai_suat:.2f}%/năm",
            hinh_thuc_lai,
            hinh_thuc_nhan
        ]
    })

    st.table(thong_tin)

    # =========================
    # BẢNG CHI TIẾT
    # =========================

    st.subheader("📊 Chi tiết tiền lãi")

    df = pd.DataFrame(du_lieu)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # CÔNG THỨC
    # =========================

    with st.expander("📖 Xem công thức tính"):

        if hinh_thuc_lai == "Lãi đơn":
            st.markdown("""
            **Công thức lãi đơn:**

            > Tiền lãi = Tiền gốc × Lãi suất năm × Số năm

            Trong đó:

            - Tiền gốc: số tiền ban đầu gửi vào ngân hàng.
            - Lãi suất năm: lãi suất tiền gửi (%/năm).
            - Số năm: kỳ hạn quy đổi về năm.

            **Ví dụ:**

            Gửi 100.000.000 VNĐ, lãi suất 6%/năm trong 12 tháng:

            > Tiền lãi = 100.000.000 × 6% × 1  
            > = **6.000.000 VNĐ**

            Tổng nhận được:

            > 100.000.000 + 6.000.000  
            > = **106.000.000 VNĐ**
            """)

        else:
            st.markdown("""
            **Công thức lãi kép:**

            > A = P × (1 + r)ⁿ

            Trong đó:

            - **P**: tiền gốc ban đầu.
            - **r**: lãi suất của mỗi kỳ nhập lãi.
            - **n**: số kỳ nhập lãi.
            - **A**: tổng tiền gốc và lãi sau kỳ hạn.

            Với hình thức lãi kép, tiền lãi của kỳ trước
            được cộng vào tiền gốc để tiếp tục tính lãi
            cho kỳ tiếp theo.
            """)
