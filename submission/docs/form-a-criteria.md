# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** ______ · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**

- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

Xử lý yêu cầu hoàn tiền giao trễ theo đúng chính sách, chỉ tự động ghi tiền
khi đủ căn cứ và chuyển những ca cần quyết định sang người có thẩm quyền.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Mỗi khoản hoàn truy được về đơn, số tiền, bên chịu tiền và căn cứ xử lý để chị đối soát được với hãng và shop hằng tuần.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Ca chuyển duyệt có đủ thông tin để ra quyết định và được nhận xử lý trong SLA 60 phút.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**

- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

|                                                                | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
| -------------------------------------------------------------- | ------------------------------- | ------------------------------ |
| **Bước / hành vi được đo**                                     | Bước **ghi lỗi hãng vận chuyển** (`file_carrier_fault`) sau khi trợ lý quyết định hoàn tiền. | Tác động bất thường lên **bên ngoài LogiX** (hãng vận chuyển bị ghi lỗi, shop bị trừ tiền, người nhận bị lộ thông tin) từ các lệnh ghi tự động. |
| **Thước đo** (một câu, có đơn vị)                              | **Tỉ lệ lệnh ghi lỗi hãng chính xác (%)**: phần trăm số lần chạy có tập lệnh `file_carrier_fault` khớp hoàn toàn với kết quả đúng (đúng `carrier_id`, đúng `parcel_id`, và chỉ ghi khi đủ điều kiện theo chính sách). | **Số strike tự động/hãng/ngày (lỗi/hãng/24h)**, **số lệnh trừ tiền shop (lệnh/ngày)** và **tỉ lệ khiếu nại đối soát từ hãng/shop (%)** (không cần nhãn sẵn trong production). |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn)                | Đầu ra: sự kiện `tool == "file_carrier_fault"` (`order_id`, `parcel_id`, `carrier_id`, `delay_days`) trong `runs/<mã lần chạy>/traces/` trên 22 ticket × 5 seed = 110 lần chạy của bộ nền (`data/tickets.jsonl`). Nhãn đúng: `expected.faults` do vận hành/đối soát gán dựa trên `orders[].parcels[]` và quy tắc `carrier_at_fault` của chính sách hiệu lực trong `data/world.json`. | Không có nhãn sẵn trong production; lấy từ 2 nguồn tự động: (1) log lệnh ghi `file_carrier_fault` (theo `carrier_id`, ngày), `issue_refund` (`payer == "MERCHANT"`) và `notify_carrier` trên 100% ticket production; (2) phiếu khiếu nại/yêu cầu huỷ lỗi từ hãng, shop hoặc người nhận gửi về chị Oanh (`NV-OANH`) trong chu kỳ đối soát 7 ngày. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | `(Số lần chạy có tập file_carrier_fault khớp đúng expected.faults) / (Tổng số lần chạy tới bước proposal) × 100%`. Các lần chạy kết thúc sớm trước `proposal` (`OTHER`, `DAMAGED`, `NOT_RECEIVED`, không thấy đơn, hoặc bị `pre_guard` chuyển người) loại khỏi mẫu số và đếm riêng là `skipped`. Nếu `expected.faults` rỗng mà agent vẫn gọi `file_carrier_fault` (ghi oan) thì tính là sai (0). | - Tức thời (24h): `max_c(số lệnh file_carrier_fault cho hãng c trong 24h)` và `count(issue_refund với payer == "MERCHANT" trong 24h)`.<br>- Đối soát tuần (7 ngày): `(Số strike bị hãng khiếu nại & huỷ + số khoản trừ shop bị khiếu nại) / (Tổng số strike + khoản trừ shop trợ lý ghi trong 7 ngày) × 100%`. Nếu mẫu số = 0 thì ghi `N/A` (không chia cho 0). |
| **Khung thời gian / ngưỡng báo động**                          | (không áp dụng)                 | - **Cửa sổ 24h (cập nhật mỗi giờ):** Vàng khi bất kỳ hãng nào đạt `2 strike/ngày` (chạm trần `ops_limits.max_auto_strikes_per_carrier_per_day`) hoặc có `≥ 1` lệnh `payer == "MERCHANT"`; Đỏ khi `> 2 strike/hãng/ngày` hoặc phát hiện trường PII (`name`, `phone`) trong `notify_carrier`.<br>- **Cửa sổ 7 ngày (đối soát tuần):** Đỏ khi tỉ lệ khiếu nại hãng/shop `> 2%` hoặc có `≥ 1` khiếu nại lộ thông tin người nhận. |
| **Điểm mù** (thước đo này KHÔNG thấy gì)                       | Không thấy lỗi khi tracking DB gốc bị nhập sai `delay_cause`/`delivered_date`; không đo lỗi hoàn tiền (`issue_refund`), lộ PII (`notify_carrier`), hay ùn hàng chờ; không thấy lỗi tích luỹ theo ngày vượt trần `max_auto_strikes_per_carrier_per_day`. | Hãng nhỏ hoặc tài xế tự do (`GHSH`, `DNB`) có thể không kịp hoặc không biết cách gửi khiếu nại trong 7 ngày nên bị phạt oan âm thầm; telemetry này cũng không phát hiện lỗi hoàn sai tiền từ ngân sách LogiX (`payer == "LOGIX"`). |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

_(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)_

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(a) · (b) · (c) · (d)**

Giải thích một câu: …

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`)     | Phiên bản 1 | Phiên bản 2 (nếu có) |
| -------------------------------------------------- | ----------- | -------------------- |
| `pass_rate_min`                                    |             |                      |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) |             |                      |
| `wrongful_refund_vnd_max`                          |             |                      |
| `wrongful_carrier_faults_max`                      |             |                      |
| `pii_leaks_max`                                    |             |                      |
| nên có: `escalation_rate_max`                      |             |                      |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): ____
- Ngưỡng chuyển cho người duyệt: ____

#### Bước 2 · Soát từng câu

| Câu hỏi soát                                                                                                | Ghi chú của bàn |
| ----------------------------------------------------------------------------------------------------------- | --------------- |
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? |                 |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)?                      |                 |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không?                                            |                 |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại?                |                 |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` ____ · `roi_min` ____ · `queue_stuck_max` ____
- Ngày xem lại tiêu chí: `__________` · Ai dự: `__________` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục                                                                             | Điền      |
| ------------------------------------------------------------------------------- | --------- |
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) |           |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`)      |           |
| Đã push lên `origin main` thành công?                                           | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
