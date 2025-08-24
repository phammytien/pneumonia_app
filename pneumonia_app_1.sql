-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1:3307
-- Thời gian đã tạo: Th8 24, 2025 lúc 06:21 PM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `pneumonia_app_1`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `activity_logs`
--

CREATE TABLE `activity_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `action` varchar(255) NOT NULL,
  `details` text DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `activity_logs`
--

INSERT INTO `activity_logs` (`id`, `user_id`, `action`, `details`, `ip_address`, `created_at`) VALUES
(1, 4, 'Chẩn đoán', 'File: NORMAL2-IM-1300-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.96%', NULL, '2025-08-21 17:23:23'),
(2, 3, 'Chẩn đoán', 'File: person151_virus_302.jpeg, KQ: Có bệnh, Độ tin cậy: 100.00%', NULL, '2025-08-22 04:21:09'),
(3, 3, 'Chẩn đoán', 'File: NORMAL2-IM-1345-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 100.00%', NULL, '2025-08-22 04:50:58'),
(4, 3, 'Chẩn đoán', 'File: NORMAL2-IM-1345-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 100.00%', NULL, '2025-08-22 04:51:53'),
(5, 3, 'Chẩn đoán', 'File: viemphoi.jpeg, KQ: Không bệnh, Độ tin cậy: 97.50%', NULL, '2025-08-22 04:51:55'),
(6, 3, 'Chẩn đoán', 'File: NORMAL2-IM-1345-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 100.00%', NULL, '2025-08-22 04:52:37'),
(7, 3, 'Chẩn đoán', 'File: viemphoi.jpeg, KQ: Không bệnh, Độ tin cậy: 97.50%', NULL, '2025-08-22 04:52:40'),
(8, 3, 'Chẩn đoán', 'File: viemphoii.jpg, KQ: Không bệnh, Độ tin cậy: 96.80%', NULL, '2025-08-22 04:52:42'),
(9, 3, 'Chẩn đoán', 'File: NORMAL2-IM-1345-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 100.00%', NULL, '2025-08-22 04:53:30'),
(10, 3, 'Chẩn đoán', 'File: viemphoi.jpeg, KQ: Không bệnh, Độ tin cậy: 97.50%', NULL, '2025-08-22 04:53:33'),
(11, 3, 'Chẩn đoán', 'File: viemphoii.jpg, KQ: Không bệnh, Độ tin cậy: 96.80%', NULL, '2025-08-22 04:53:36'),
(12, 3, 'Chẩn đoán', 'File: person9_bacteria_39.jpeg, KQ: Có bệnh, Độ tin cậy: 100.00%', NULL, '2025-08-22 04:53:36'),
(13, 4, 'Chẩn đoán', 'File: person9_bacteria_39.jpeg, KQ: Có bệnh, Độ tin cậy: 100.00%', NULL, '2025-08-22 04:57:24'),
(14, 4, 'Chẩn đoán', 'File: person896_bacteria_2821.jpeg, KQ: Có bệnh, Độ tin cậy: 100.00%', NULL, '2025-08-22 05:02:05'),
(15, 4, 'Chẩn đoán', 'File: person98_virus_182.jpeg, KQ: Có bệnh, Độ tin cậy: 100.00%', NULL, '2025-08-22 05:06:50'),
(16, 4, 'Chẩn đoán', 'File: person98_virus_182.jpeg, KQ: Có bệnh, Độ tin cậy: 100.00%', NULL, '2025-08-22 05:06:56'),
(17, 4, 'Chẩn đoán', 'File: person98_virus_182.jpeg, KQ: Có bệnh, Độ tin cậy: 100.00%', NULL, '2025-08-22 05:07:00'),
(18, 4, 'Chẩn đoán', 'File: person98_virus_182.jpeg, KQ: Có bệnh, Độ tin cậy: 100.00%', NULL, '2025-08-22 05:07:07'),
(19, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1346-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 100.00%', NULL, '2025-08-22 05:17:05'),
(20, 4, 'Chẩn đoán', 'File: NORMAL2-IM-1349-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.93%', NULL, '2025-08-22 05:18:55'),
(21, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1362-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.83%', NULL, '2025-08-22 05:20:12'),
(22, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1333-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.44%', NULL, '2025-08-22 05:21:40'),
(23, 4, 'Chẩn đoán', 'File: NORMAL2-IM-1345-0001-0002.jpeg, KQ: Không bệnh, Độ tin cậy: 99.98%', NULL, '2025-08-22 05:23:06'),
(24, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1333-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.44%', NULL, '2025-08-22 05:26:42'),
(25, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1334-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.98%', NULL, '2025-08-22 05:28:13'),
(26, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1334-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.98%', NULL, '2025-08-22 05:28:31'),
(27, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1334-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.98%', NULL, '2025-08-22 05:28:33'),
(28, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1334-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.98%', NULL, '2025-08-22 05:28:39'),
(29, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1333-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.44%', NULL, '2025-08-22 05:31:10'),
(30, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1356-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 91.21%', NULL, '2025-08-22 05:33:27'),
(31, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1345-0001-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.93%', NULL, '2025-08-22 05:34:59'),
(32, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1345-0001-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.93%', NULL, '2025-08-22 05:35:17'),
(33, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1345-0001-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.93%', NULL, '2025-08-22 05:35:23'),
(34, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1345-0001-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.93%', NULL, '2025-08-22 05:35:44'),
(35, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1345-0001-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.93%', NULL, '2025-08-22 05:36:09'),
(36, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1334-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.98%', NULL, '2025-08-22 05:37:06'),
(37, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1376-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 97.34%', NULL, '2025-08-22 05:39:09'),
(38, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1376-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 97.34%', NULL, '2025-08-22 05:39:18'),
(39, 5, 'Chẩn đoán', 'File: NORMAL2-IM-1376-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 97.34%', NULL, '2025-08-22 05:39:21'),
(40, 4, 'Chẩn đoán', 'File: NORMAL2-IM-1334-0001.jpeg, KQ: Không bệnh, Độ tin cậy: 99.98%', NULL, '2025-08-22 05:40:18');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `admin_replies`
--

CREATE TABLE `admin_replies` (
  `id` int(11) NOT NULL,
  `feedback_id` int(11) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `admin_name` varchar(50) NOT NULL,
  `reply` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `admin_replies`
--

INSERT INTO `admin_replies` (`id`, `feedback_id`, `admin_id`, `admin_name`, `reply`, `created_at`) VALUES
(1, 2, 3, 'admin', 'không tốt', '2025-08-23 11:28:29'),
(3, 5, 3, 'admin', 'cảm ơn nhé', '2025-08-23 12:54:15'),
(4, 6, 3, 'admin', 'sao tui có thể giúp dì', '2025-08-23 13:12:43');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `feedbacks`
--

CREATE TABLE `feedbacks` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `rating` int(11) DEFAULT NULL CHECK (`rating` between 1 and 5),
  `comment` text DEFAULT NULL,
  `phan_hoi_admin` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `feedbacks`
--

INSERT INTO `feedbacks` (`id`, `user_id`, `username`, `rating`, `comment`, `phan_hoi_admin`, `created_at`, `updated_at`) VALUES
(2, 6, 'minhanh', 1, 'ứng dụng dùng tốt chứ\n', NULL, '2025-08-23 11:27:55', '2025-08-23 11:27:55'),
(5, 7, 'honganh', 5, 'ứng dụng ok\n', NULL, '2025-08-23 12:53:33', '2025-08-23 12:53:33'),
(6, 7, 'honganh', 2, 'hmm', NULL, '2025-08-23 13:07:47', '2025-08-23 13:07:47'),
(7, 4, 'teone', 5, 'ok', NULL, '2025-08-24 15:01:36', '2025-08-24 15:01:36'),
(8, 4, 'teone', 5, 'tốt', NULL, '2025-08-24 16:05:50', '2025-08-24 16:05:50');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `lich_su_chan_doan`
--

CREATE TABLE `lich_su_chan_doan` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `result` varchar(255) DEFAULT NULL,
  `algorithm` varchar(50) DEFAULT 'YOLO11',
  `confidence` float DEFAULT 0,
  `severity` varchar(50) DEFAULT NULL,
  `recommendation` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `lich_su_chan_doan`
--

INSERT INTO `lich_su_chan_doan` (`id`, `user_id`, `username`, `filename`, `result`, `algorithm`, `confidence`, `severity`, `recommendation`, `created_at`) VALUES
(1, 4, 'teone', 'NORMAL2-IM-1332-0001.jpeg', 'Không bệnh', 'YOLO11', 0.999991, 'Trung bình', 'Cần xét nghiệm thêm để xác định', '2025-08-21 13:41:09'),
(2, 4, 'teone', 'NORMAL2-IM-1335-0001.jpeg', 'Không bệnh', 'YOLO11', 0.999993, 'Trung bình', 'Cần xét nghiệm thêm để xác định', '2025-05-21 13:41:51'),
(3, 4, 'teone', 'person88_virus_164.jpeg', 'Có bệnh', 'YOLO11', 0.99997, 'Nặng', 'Cần xét nghiệm thêm để xác định', '2025-08-21 13:44:03'),
(4, 4, 'teone', 'person9_bacteria_41.jpeg', 'Có bệnh', 'YOLO11', 0.999997, 'Nặng', 'Cần xét nghiệm thêm', '2025-06-21 14:03:34'),
(5, 4, 'teone', 'person9_bacteria_40.jpeg', 'Có bệnh', 'YOLO11', 100, 'Nặng', 'Cần nhập viện ngay để điều trị khẩn cấp', '2025-08-21 16:01:28'),
(6, 4, 'teone', 'NORMAL2-IM-1334-0001.jpeg', 'Không bệnh', 'YOLO11', 99.983, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-21 16:05:38'),
(7, 4, 'teone', '112.jpg', 'Có bệnh', 'YOLO11', 68.9503, 'Trung bình', 'Nên đi khám bác sĩ để được kiểm tra chi tiết', '2025-07-21 16:32:56'),
(8, 5, 'tien', '1902.jpg', 'Có bệnh', 'YOLO11', 62.7619, 'Trung bình', 'Nên đi khám bác sĩ để được kiểm tra chi tiết', '2025-08-21 16:38:55'),
(9, 5, 'tien', '1902.jpg', 'Có bệnh', 'YOLO11', 62.7619, 'Trung bình', 'Nên đi khám bác sĩ để được kiểm tra chi tiết', '2025-08-21 16:40:57'),
(10, 4, 'teone', 'NORMAL2-IM-1347-0001.jpeg', 'Không bệnh', 'YOLO11', 99.9969, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-06-21 16:57:31'),
(11, 3, 'admin', 'NORMAL2-IM-1335-0001.jpeg', 'Không bệnh', 'YOLO11', 99.9993, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-21 17:14:11'),
(12, 4, 'teone', 'NORMAL2-IM-1350-0001.jpeg', 'Không bệnh', 'YOLO11', 99.999, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-21 17:16:00'),
(13, 4, 'teone', 'NORMAL2-IM-1300-0001.jpeg', 'Không bệnh', 'YOLO11', 99.9629, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-21 17:23:23'),
(14, 3, 'admin', 'person151_virus_302.jpeg', 'Có bệnh', 'YOLO11', 99.9997, 'Nặng', 'Cần nhập viện ngay để điều trị khẩn cấp', '2025-08-22 04:21:09'),
(15, 3, 'admin', 'NORMAL2-IM-1345-0001.jpeg', 'Không bệnh', 'YOLO11', 100, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-22 04:50:58'),
(16, 3, 'admin', 'NORMAL2-IM-1345-0001.jpeg', 'Không bệnh', 'YOLO11', 100, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-22 04:51:53'),
(17, 3, 'admin', 'viemphoi.jpeg', 'Không bệnh', 'YOLO11', 97.5037, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-22 04:51:55'),
(18, 3, 'admin', 'NORMAL2-IM-1345-0001.jpeg', 'Không bệnh', 'YOLO11', 100, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-22 04:52:37'),
(19, 3, 'admin', 'viemphoi.jpeg', 'Không bệnh', 'YOLO11', 97.5037, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-22 04:52:40'),
(20, 3, 'admin', 'viemphoii.jpg', 'Không bệnh', 'YOLO11', 96.8036, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-22 04:52:42'),
(21, 3, 'admin', 'NORMAL2-IM-1345-0001.jpeg', 'Không bệnh', 'YOLO11', 100, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-22 04:53:30'),
(22, 3, 'admin', 'viemphoi.jpeg', 'Không bệnh', 'YOLO11', 97.5037, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-22 04:53:33'),
(23, 3, 'admin', 'viemphoii.jpg', 'Không bệnh', 'YOLO11', 96.8036, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-22 04:53:35'),
(24, 3, 'admin', 'person9_bacteria_39.jpeg', 'Có bệnh', 'YOLO11', 100, 'Nặng', 'Cần nhập viện ngay để điều trị khẩn cấp', '2025-08-22 04:53:36'),
(25, 4, 'teone', 'person9_bacteria_39.jpeg', 'Có bệnh', 'YOLO11', 100, 'Nặng', 'Cần nhập viện ngay để điều trị khẩn cấp', '2025-08-22 04:57:24'),
(26, 4, 'teone', 'person896_bacteria_2821.jpeg', 'Có bệnh', 'YOLO11', 100, 'Nặng', 'Cần nhập viện ngay để điều trị khẩn cấp', '2025-08-22 05:02:05'),
(27, 4, 'teone', 'person98_virus_182.jpeg', 'Có bệnh', 'YOLO11', 100, 'Nặng', 'Cần nhập viện ngay để điều trị khẩn cấp', '2025-08-22 05:06:50'),
(28, 4, 'teone', 'person98_virus_182.jpeg', 'Có bệnh', 'YOLO11', 100, 'Nặng', 'Cần nhập viện ngay để điều trị khẩn cấp', '2025-08-22 05:06:56'),
(29, 4, 'teone', 'person98_virus_182.jpeg', 'Có bệnh', 'YOLO11', 100, 'Nặng', 'Cần nhập viện ngay để điều trị khẩn cấp', '2025-07-22 05:07:00'),
(30, 4, 'teone', 'person98_virus_182.jpeg', 'Có bệnh', 'YOLO11', 100, 'Nặng', 'Cần nhập viện ngay để điều trị khẩn cấp', '2025-08-22 05:07:07'),
(31, 5, 'tien', 'NORMAL2-IM-1346-0001.jpeg', 'Không bệnh', 'YOLO11', 100, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-06-22 05:17:05'),
(32, 4, 'teone', 'NORMAL2-IM-1349-0001.jpeg', 'Không bệnh', 'YOLO11', 99.9287, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-06-22 05:18:55'),
(33, 5, 'tien', 'NORMAL2-IM-1362-0001.jpeg', 'Không bệnh', 'YOLO11', 99.8285, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-22 05:20:12'),
(34, 5, 'tien', 'NORMAL2-IM-1333-0001.jpeg', 'Không bệnh', 'YOLO11', 99.4399, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-22 05:21:40'),
(35, 4, 'teone', 'NORMAL2-IM-1345-0001-0002.jpeg', 'Không bệnh', 'YOLO11', 99.9757, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-07-22 05:23:06'),
(36, 5, 'tien', 'NORMAL2-IM-1333-0001.jpeg', 'Không bệnh', 'YOLO11', 99.4399, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-22 05:26:42'),
(37, 5, 'tien', 'NORMAL2-IM-1334-0001.jpeg', 'Không bệnh', 'YOLO11', 99.983, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-07-22 05:28:13'),
(38, 5, 'tien', 'NORMAL2-IM-1334-0001.jpeg', 'Không bệnh', 'YOLO11', 99.983, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-06-22 05:28:31'),
(39, 5, 'tien', 'NORMAL2-IM-1334-0001.jpeg', 'Không bệnh', 'YOLO11', 99.983, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-22 05:28:33'),
(40, 5, 'tien', 'NORMAL2-IM-1334-0001.jpeg', 'Không bệnh', 'YOLO11', 99.983, 'Không phát hiện', 'Tiếp tục duy trì lối sống lành mạnh, kiểm tra sức khỏe định kỳ', '2025-08-22 05:28:39');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `full_name`, `email`, `phone`, `address`, `avatar`, `role`, `created_at`) VALUES
(1, 'user1', '123456', 'Nguyễn Văn An', 'user1@example.com', NULL, NULL, '4444.jpg', 'user', '2025-08-21 13:39:21'),
(2, 'user2', '123456', 'Trần Thị Bình', 'user2@example.com', NULL, NULL, '4444.jpg', 'user', '2025-08-21 13:39:21'),
(3, 'admin', 'scrypt:32768:8:1$UsN2UTs4sIZ4J67F$777d5a624de12d58b0b79883662f3e34c014313db90a154fd4cd9f82f336728bba45b634486ce0c161ae006abbb8544dc85daa0de2a9d301f910248b52650373', 'Quản trị viên', 'admin@example.com', NULL, NULL, '4444.jpg', 'admin', '2025-08-21 13:40:34'),
(4, 'teone', 'scrypt:32768:8:1$lenDSL0X8mdsiDp5$fbce9b0bfc3335f99cfea052de903de618f0a4cc8b1b7a283d0e60ef5da47fc1aa5d9a79e2951414255cf33a6d28639c03bc230c9194c9ee66a9fb5dc6861797', 'Tèo Em là tôi', 'teo@gmail.com', '0321456987', 'Cao Lãnh', '4444.jpg', 'user', '2025-08-21 13:40:59'),
(5, 'tien', 'scrypt:32768:8:1$haerKRRsm2MtxZ0x$4ab4c916e998ef18fdd9c1f182a942a1779e6566f5564023604277c18e750f73c6caf1408473f2506ca3f29084cf96f1b333d83ffc2091f92135c1ea50dfd5f7', NULL, NULL, NULL, NULL, NULL, 'user', '2025-08-21 16:35:42'),
(6, 'minhanh', 'scrypt:32768:8:1$OZOlXaNyh5a9q2so$cd5955702825017f318434c1833cfb9dd9682ed6ac816a669c0aa95a59bb0e0ef7a34a5fc8753ab28b6a5dcaae62eeb43bc9113800e04e60cef0e6b66cc05473', NULL, NULL, NULL, NULL, NULL, 'user', '2025-08-23 10:51:31'),
(7, 'honganh', 'scrypt:32768:8:1$cxZgOyrACx2Is2nE$784ded5033e038bf91544f9e7800d8be2f2795f1dc24b1a98422007df5a3e20f90c8cce23ca8bc69d06a01604cedfa7fd3e665d0cbe05749bebd38671614e5d4', NULL, NULL, NULL, NULL, NULL, 'user', '2025-08-23 12:49:34');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Chỉ mục cho bảng `admin_replies`
--
ALTER TABLE `admin_replies`
  ADD PRIMARY KEY (`id`),
  ADD KEY `feedback_id` (`feedback_id`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Chỉ mục cho bảng `feedbacks`
--
ALTER TABLE `feedbacks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Chỉ mục cho bảng `lich_su_chan_doan`
--
ALTER TABLE `lich_su_chan_doan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Chỉ mục cho bảng `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `activity_logs`
--
ALTER TABLE `activity_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=191;

--
-- AUTO_INCREMENT cho bảng `admin_replies`
--
ALTER TABLE `admin_replies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT cho bảng `feedbacks`
--
ALTER TABLE `feedbacks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT cho bảng `lich_su_chan_doan`
--
ALTER TABLE `lich_su_chan_doan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=203;

--
-- AUTO_INCREMENT cho bảng `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD CONSTRAINT `activity_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Các ràng buộc cho bảng `admin_replies`
--
ALTER TABLE `admin_replies`
  ADD CONSTRAINT `admin_replies_ibfk_1` FOREIGN KEY (`feedback_id`) REFERENCES `feedbacks` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `admin_replies_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Các ràng buộc cho bảng `feedbacks`
--
ALTER TABLE `feedbacks`
  ADD CONSTRAINT `feedbacks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Các ràng buộc cho bảng `lich_su_chan_doan`
--
ALTER TABLE `lich_su_chan_doan`
  ADD CONSTRAINT `lich_su_chan_doan_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
