# Team

## Thông tin nhóm

- Tên nhóm: `777`
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-Day10-777-PoCtoPilotGate1`
- Thẻ sự cố đã bốc: `S7`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Trần Quang Hưng | 2A202603767 | Vận hành và pháp lý |      X       |
|   2 | Nguyễn Tiến Đạt | 2A202603752 | Kỹ sư cổng |             |
|   3 | Cao Phạm Tân Khải | 2A202603883 | Kỹ sư cổng |             |
|   4 | Nguyễn Quang Huy | 2A202603768 | Sản phẩm và kinh doanh |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Các mục dưới đây dựa trên phiếu và lịch sử commit. Từng thành viên xác nhận đóng góp, exit ticket và bổ sung phần sử dụng AI của mình nếu có theo [quy định lab](RULES.md#ai-và-công-cụ).

## TranQuangHung-2A202603767

- **Phụ trách** — Trưởng nhóm, vận hành và pháp lý. A5, B7.5–B8 và C11–C12.
- **Đóng góp** — Ký tiêu chí, chốt cổng vòng 1 và ghi quyết định v1. Phụ trách runbook vận hành và quyết định Gate 1.
- **Bằng chứng** — `014231f`, `784541c`, Phiếu B mục B8 và Phiếu C mục C12.
- **Exit ticket (nháp)** — Cần ký tiêu chí trước khi đo để có căn cứ quyết định. Còn cần kiểm tra thời gian dừng luồng tự động khi ca trực nhận cảnh báo lộ dữ liệu.

## NguyenTienDat-2A202603752

- **Phụ trách** — Kỹ sư cổng. Chất lượng và quyền hạn ở B5, C11.
- **Đóng góp** — Cập nhật Phiếu A ở A1. Là PIC đối chiếu kết quả hồi quy và kiểm quyền gọi lệnh ghi.
- **Bằng chứng** — `0882bf2`, Phiếu B mục B5 dòng 1 và 4, Phiếu C mục C11 dòng 1 và 4, report `R-S7-grade-20261119-194748-03db1f`.
- **Exit ticket (nháp)** — Kiểm hồi quy giúp phát hiện cổng mới làm hỏng ca từng đúng. Còn cần xác minh kết quả trên bộ test ẩn.

## CaoPhamTanKhai-2A202603883

- **Phụ trách** — Kỹ sư cổng. Soát trace, bảo mật và hiệu năng.
- **Đóng góp** — Cập nhật A2–A3, phân tích lỗi trong trace `T-002@55` ở B2 và bổ sung pre-mortem ở B6.
- **Bằng chứng** — `ea01616`, `b2e18b6`, `407cfcf`, `1a673b5`, Phiếu C mục C11 dòng 3.
- **Exit ticket (nháp)** — Trace giúp truy từ khoản hoàn sai về bước ghi đè số ngày trễ. Còn cần kiểm giá trị nhạy cảm có thể nằm trong trường `district` hợp lệ.

## NguyenQuangHuy-2A202603768

- **Phụ trách** — Sản phẩm và kinh doanh. Tiêu chí Phiếu A, dữ liệu và chi phí ở B5 và C11.
- **Đóng góp** — Cập nhật tiêu chí ở A4 và bảng HAZOP ở B4. Là PIC đối chiếu nguồn dữ liệu và chi phí trong checklist go-live.
- **Bằng chứng** — `1b01ffe`, `bf1ea2d`, Phiếu B mục B5 dòng 2 và 6, Phiếu C mục C11 dòng 6.
- **Exit ticket (nháp)** — Chi phí và ROI cần được đọc cùng tải duyệt. Còn cần đo lại hai chỉ số này ở giờ cao điểm trong pilot.
