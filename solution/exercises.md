# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Sau khi thử các giá trị temperature tương ứng, tôi thấy mô hình sinh ra câu trả lời dần thay đổi từ khô khan, cứng nhắc sang sáng tạo hơn. Tuy nhiên, ở mức 1.5 bắt đầu có sự ảo giác (những câu đầu nó nói về hang Sơn-DDooong nhưng cuối cùng lại chốt là lúa gạo)

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
>Tùy vào đối tượng khách hàng: với những người yêu cầu sự chính xác thì cần đặt temperature thấp thuộc khoảng [0.1,0.3], với người cần sáng tạo thì cần phải đặt cao hơn khoảng [0.6, 0.9]

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem gemini-2.5-flash đắt hơn gemin-2.5-flash-lite bao nhiêu lần cho workload này:**
> workload = 350x10000x3 = 10.5m token
thực tế giá token cho flash đắt hơn flash-lite khoảng 15-20 lần nên workload cũng đắt hơn khoảng từng đó

**Mô tả một trường hợp mà chi phí cao hơn của gemini-2.5-flash là xứng đáng, và một trường hợp gemini-2.5-flash-lite là lựa chọn tốt hơn:**
> Trường hợp mà 2.5 flash tốt hơn: hi cần xử lý các tác vụ yêu cầu suy luận logic đa tầng, phân tích hình ảnh phức tạp, hoặc viết code tối ưu, ví dụ: Một trợ lý ảo tư vấn luật hoặc chính sách. Trường hợp mà 2.5 flash-lite tốt hơn: khi cần xử lý các tác vụ đơn giản (có thể quy mô lớn): phân tích cảm xúc khách hàng, trích xuất thông tin.


---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Dựa vào kết quả latency, bản flash mất tới 2.55s để trả về kết quả hoàn chỉnh — một khoảng thời gian đủ lâu để người dùng cảm thấy ứng dụng bị treo, gây trải nghiệm tệ. Streaming giúp hiển thị văn bản ngay lập tức khi chúng được tạo ra, giảm Thời gian phản hồi đầu tiên xuống mức mili giây, tạo cảm giác AI đang ngay lập tức phản hồi. Vì vậy model gemini 2.5 flash không phù hợp với Streaming. Tuy nhiên, Non-streaming lại phù hợp hơn cho các tác vụ chạy ngầm (Background) như gửi email tự động sau khi tổng hợp xong dữ liệu, hoặc khi hệ thống cần nhận đủ file JSON hoàn chỉnh để thực hiện các bước xử lý logic tiếp theo trong mã nguồn.


## Danh Sách Kiểm Tra Nộp Bài
- [x] Tất cả tests pass: `pytest tests/ -v`
- [x] `call_openai` đã triển khai và kiểm thử
- [x] `call_openai_mini` đã triển khai và kiểm thử
- [x] `compare_models` đã triển khai và kiểm thử
- [x] `streaming_chatbot` đã triển khai và kiểm thử
- [x] `retry_with_backoff` đã triển khai và kiểm thử
- [x] `batch_compare` đã triển khai và kiểm thử
- [x] `format_comparison_table` đã triển khai và kiểm thử
- [x] `exercises.md` đã điền đầy đủ
- [x] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
