CREATE TABLE IF NOT EXISTS EmployeeUoB (
  EmployeeID INT NOT NULL PRIMARY KEY,
  title VARCHAR(12) NOT NULL,
  forename VARCHAR(255) NOT NULL,
  surname VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  salary INT NOT NULL
);

INSERT INTO EmployeeUoB VALUES (0, 'Mr', 'Richard', 'Hendricks', 'ceo@piedpiper.com', 1234);
INSERT INTO EmployeeUoB VALUES (1, 'Mr', 'Jared', 'dunn', 'j.dunn@piedpiper.com', 123);
INSERT INTO EmployeeUoB VALUES (2, 'Mr', 'Erlich', 'Bachman', 'ceo@startupindustries.com', 0);
INSERT INTO EmployeeUoB VALUES (3, 'Mr', 'Nelson', 'Bighettu', 'cs@sandford.edu', 1234);
INSERT INTO EmployeeUoB VALUES (4, 'Ms', 'Monica', 'Hall', 'm.hall@bream-hall.com', 123445);
INSERT INTO EmployeeUoB VALUES (5, 'Mr', 'Dinesh', 'Chugtai', 'd.chugtai@piedpiper.com', 12);
INSERT INTO EmployeeUoB VALUES (6, 'Mr', 'Bertram', 'Gilfoyle', 'b.gilfoyle@protonmail.ch', 1288);
INSERT INTO EmployeeUoB VALUES (7, 'Mr', 'Gavin', 'Belson', 'ceo@hooli.net', 2500000);
