--- 실행방법
--- mysql -u its -p its_web < add_viewer.sql

UPDATE g5_board SET bo_list_level = 5, bo_read_level = 5;


INSERT INTO `g5_member` (`mb_no`, `mb_id`, `mb_password`, `mb_name`, `mb_nick`, `mb_nick_date`, `mb_email`, `mb_homepage`, `mb_level`, `mb_sex`, `mb_birth`, `mb_tel`, `mb_hp`, `mb_certify`, `mb_adult`, `mb_dupinfo`, `mb_zip1`, `mb_zip2`, `mb_addr1`, `mb_addr2`, `mb_addr3`, `mb_addr_jibeon`, `mb_signature`, `mb_recommend`, `mb_point`, `mb_today_login`, `mb_login_ip`, `mb_datetime`, `mb_ip`, `mb_leave_date`, `mb_intercept_date`, `mb_email_certify`, `mb_email_certify2`, `mb_memo`, `mb_lost_certify`, `mb_mailling`, `mb_sms`, `mb_open`, `mb_open_date`, `mb_profile`, `mb_memo_call`, `mb_memo_cnt`, `mb_scrap_cnt`, `mb_1`, `mb_2`, `mb_3`, `mb_4`, `mb_5`, `mb_6`, `mb_7`, `mb_8`, `mb_9`, `mb_10`) VALUES
(4, 'viewer', 'sha256:12000:y+f8p1pil7PyycyABPQbZJ1uosIWsFdf:W7sfNkQg5mCvMMzpFDxVtkhFSFQQQLDQ', '담당자', '담당자', '0000-00-00', 'viewer@its.com', '', 5, '', '', '', '', '', 0, '', '', '', '', '', '', '', '', '', 0, '2020-12-18 01:30:34', '192.168.0.2', '2020-12-17 14:00:42', '192.168.0.2', '', '', '2020-12-17 14:00:42', '', '', '', 0, 0, 0, '2020-12-17', '', '', 0, 0, '', '', '', '', '', '', '', '', '', '');