"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H
from .tools import Verdict


def pre_guard(ctx):
    return Verdict.allow()


def write_gate(ctx, action):
    tool = action["tool"]
    if tool not in ("issue_refund", "file_carrier_fault", "notify_carrier"):
        return Verdict.allow()

    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.deny("không có chính sách hoàn tiền còn hiệu lực")

    if tool == "notify_carrier":
        original = action["payload"]
        fields = policy["carrier_notice_fields"]
        payload = {key: value for key, value in original.items() if key in fields}
        if payload != original:
            return Verdict.modify("chỉ gửi hãng các trường được chính sách cho phép", payload=payload)
        return Verdict.allow()

    order = ctx.tools.lookup_order(action["order_id"])
    if order is None or not order["parcels"]:
        return Verdict.deny("không có tracking của đơn")
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    delay = H.db_delay_days(parcel, ctx.as_of)

    if tool == "issue_refund":
        entitlement = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
        if action["amount_vnd"] > entitlement:
            return Verdict.deny("tiền hoàn vượt quyền lợi tính từ tracking và chính sách")
    else:
        if action["parcel_id"] != parcel["parcel_id"] or action["carrier_id"] != parcel["carrier_id"]:
            return Verdict.deny("kiện hoặc hãng không khớp tracking của yêu cầu")
        if not H.carrier_at_fault(policy, parcel, delay):
            return Verdict.deny("tracking không đủ căn cứ ghi lỗi hãng")
        if action["delay_days"] != delay:
            return Verdict.modify("dùng độ trễ của kiện trong tracking", delay_days=delay)

    return Verdict.allow()
