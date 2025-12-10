-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-12-2025 a las 20:00:20
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `nutriologo`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administrador`
--

CREATE TABLE `administrador` (
  `id_administrador` int(11) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `contrasena` varchar(100) NOT NULL,
  `activo` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `administrador`
--

INSERT INTO `administrador` (`id_administrador`, `nombre`, `telefono`, `correo`, `contrasena`, `activo`) VALUES
(1, 'rafa', '1234567890', 'rafa@gmail.com', '123456', 1),
(2, 'Miguel Angel Rosales Soto', '0987654321', 'rnz@gmail.com', '123456', 1),
(3, 'qweqwe', '123123123123', 'qwe@qwe.qwe', 'qweqwe', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `id_cita` int(11) NOT NULL,
  `id_paciente` int(11) NOT NULL,
  `id_horario` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora_cita` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `citas`
--

INSERT INTO `citas` (`id_cita`, `id_paciente`, `id_horario`, `fecha`, `hora_cita`) VALUES
(1, 1, 144, '2025-10-01', '19:50:00'),
(2, 2, 121, '2025-10-01', '16:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horarios_disponibles`
--

CREATE TABLE `horarios_disponibles` (
  `id_horario` int(11) NOT NULL,
  `dia_semana` varchar(20) NOT NULL,
  `hora` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `horarios_disponibles`
--

INSERT INTO `horarios_disponibles` (`id_horario`, `dia_semana`, `hora`) VALUES
(1, 'Lunes', '10:00:00'),
(2, 'Lunes', '10:10:00'),
(3, 'Lunes', '10:20:00'),
(4, 'Lunes', '10:30:00'),
(5, 'Lunes', '10:40:00'),
(6, 'Lunes', '10:50:00'),
(7, 'Lunes', '11:00:00'),
(8, 'Lunes', '11:10:00'),
(9, 'Lunes', '11:20:00'),
(10, 'Lunes', '11:30:00'),
(11, 'Lunes', '11:40:00'),
(12, 'Lunes', '11:50:00'),
(13, 'Lunes', '12:00:00'),
(14, 'Lunes', '12:10:00'),
(15, 'Lunes', '12:20:00'),
(16, 'Lunes', '12:30:00'),
(17, 'Lunes', '12:40:00'),
(18, 'Lunes', '12:50:00'),
(19, 'Lunes', '13:00:00'),
(20, 'Lunes', '13:10:00'),
(21, 'Lunes', '13:20:00'),
(22, 'Lunes', '13:30:00'),
(23, 'Lunes', '13:40:00'),
(24, 'Lunes', '13:50:00'),
(25, 'Lunes', '16:00:00'),
(26, 'Lunes', '16:10:00'),
(27, 'Lunes', '16:20:00'),
(28, 'Lunes', '16:30:00'),
(29, 'Lunes', '16:40:00'),
(30, 'Lunes', '16:50:00'),
(31, 'Lunes', '17:00:00'),
(32, 'Lunes', '17:10:00'),
(33, 'Lunes', '17:20:00'),
(34, 'Lunes', '17:30:00'),
(35, 'Lunes', '17:40:00'),
(36, 'Lunes', '17:50:00'),
(37, 'Lunes', '18:00:00'),
(38, 'Lunes', '18:10:00'),
(39, 'Lunes', '18:20:00'),
(40, 'Lunes', '18:30:00'),
(41, 'Lunes', '18:40:00'),
(42, 'Lunes', '18:50:00'),
(43, 'Lunes', '19:00:00'),
(44, 'Lunes', '19:10:00'),
(45, 'Lunes', '19:20:00'),
(46, 'Lunes', '19:30:00'),
(47, 'Lunes', '19:40:00'),
(48, 'Lunes', '19:50:00'),
(49, 'Martes', '10:00:00'),
(50, 'Martes', '10:10:00'),
(51, 'Martes', '10:20:00'),
(52, 'Martes', '10:30:00'),
(53, 'Martes', '10:40:00'),
(54, 'Martes', '10:50:00'),
(55, 'Martes', '11:00:00'),
(56, 'Martes', '11:10:00'),
(57, 'Martes', '11:20:00'),
(58, 'Martes', '11:30:00'),
(59, 'Martes', '11:40:00'),
(60, 'Martes', '11:50:00'),
(61, 'Martes', '12:00:00'),
(62, 'Martes', '12:10:00'),
(63, 'Martes', '12:20:00'),
(64, 'Martes', '12:30:00'),
(65, 'Martes', '12:40:00'),
(66, 'Martes', '12:50:00'),
(67, 'Martes', '13:00:00'),
(68, 'Martes', '13:10:00'),
(69, 'Martes', '13:20:00'),
(70, 'Martes', '13:30:00'),
(71, 'Martes', '13:40:00'),
(72, 'Martes', '13:50:00'),
(73, 'Martes', '16:00:00'),
(74, 'Martes', '16:10:00'),
(75, 'Martes', '16:20:00'),
(76, 'Martes', '16:30:00'),
(77, 'Martes', '16:40:00'),
(78, 'Martes', '16:50:00'),
(79, 'Martes', '17:00:00'),
(80, 'Martes', '17:10:00'),
(81, 'Martes', '17:20:00'),
(82, 'Martes', '17:30:00'),
(83, 'Martes', '17:40:00'),
(84, 'Martes', '17:50:00'),
(85, 'Martes', '18:00:00'),
(86, 'Martes', '18:10:00'),
(87, 'Martes', '18:20:00'),
(88, 'Martes', '18:30:00'),
(89, 'Martes', '18:40:00'),
(90, 'Martes', '18:50:00'),
(91, 'Martes', '19:00:00'),
(92, 'Martes', '19:10:00'),
(93, 'Martes', '19:20:00'),
(94, 'Martes', '19:30:00'),
(95, 'Martes', '19:40:00'),
(96, 'Martes', '19:50:00'),
(97, 'Miércoles', '10:00:00'),
(98, 'Miércoles', '10:10:00'),
(99, 'Miércoles', '10:20:00'),
(100, 'Miércoles', '10:30:00'),
(101, 'Miércoles', '10:40:00'),
(102, 'Miércoles', '10:50:00'),
(103, 'Miércoles', '11:00:00'),
(104, 'Miércoles', '11:10:00'),
(105, 'Miércoles', '11:20:00'),
(106, 'Miércoles', '11:30:00'),
(107, 'Miércoles', '11:40:00'),
(108, 'Miércoles', '11:50:00'),
(109, 'Miércoles', '12:00:00'),
(110, 'Miércoles', '12:10:00'),
(111, 'Miércoles', '12:20:00'),
(112, 'Miércoles', '12:30:00'),
(113, 'Miércoles', '12:40:00'),
(114, 'Miércoles', '12:50:00'),
(115, 'Miércoles', '13:00:00'),
(116, 'Miércoles', '13:10:00'),
(117, 'Miércoles', '13:20:00'),
(118, 'Miércoles', '13:30:00'),
(119, 'Miércoles', '13:40:00'),
(120, 'Miércoles', '13:50:00'),
(121, 'Miércoles', '16:00:00'),
(122, 'Miércoles', '16:10:00'),
(123, 'Miércoles', '16:20:00'),
(124, 'Miércoles', '16:30:00'),
(125, 'Miércoles', '16:40:00'),
(126, 'Miércoles', '16:50:00'),
(127, 'Miércoles', '17:00:00'),
(128, 'Miércoles', '17:10:00'),
(129, 'Miércoles', '17:20:00'),
(130, 'Miércoles', '17:30:00'),
(131, 'Miércoles', '17:40:00'),
(132, 'Miércoles', '17:50:00'),
(133, 'Miércoles', '18:00:00'),
(134, 'Miércoles', '18:10:00'),
(135, 'Miércoles', '18:20:00'),
(136, 'Miércoles', '18:30:00'),
(137, 'Miércoles', '18:40:00'),
(138, 'Miércoles', '18:50:00'),
(139, 'Miércoles', '19:00:00'),
(140, 'Miércoles', '19:10:00'),
(141, 'Miércoles', '19:20:00'),
(142, 'Miércoles', '19:30:00'),
(143, 'Miércoles', '19:40:00'),
(144, 'Miércoles', '19:50:00'),
(145, 'Jueves', '10:00:00'),
(146, 'Jueves', '10:10:00'),
(147, 'Jueves', '10:20:00'),
(148, 'Jueves', '10:30:00'),
(149, 'Jueves', '10:40:00'),
(150, 'Jueves', '10:50:00'),
(151, 'Jueves', '11:00:00'),
(152, 'Jueves', '11:10:00'),
(153, 'Jueves', '11:20:00'),
(154, 'Jueves', '11:30:00'),
(155, 'Jueves', '11:40:00'),
(156, 'Jueves', '11:50:00'),
(157, 'Jueves', '12:00:00'),
(158, 'Jueves', '12:10:00'),
(159, 'Jueves', '12:20:00'),
(160, 'Jueves', '12:30:00'),
(161, 'Jueves', '12:40:00'),
(162, 'Jueves', '12:50:00'),
(163, 'Jueves', '13:00:00'),
(164, 'Jueves', '13:10:00'),
(165, 'Jueves', '13:20:00'),
(166, 'Jueves', '13:30:00'),
(167, 'Jueves', '13:40:00'),
(168, 'Jueves', '13:50:00'),
(169, 'Jueves', '16:00:00'),
(170, 'Jueves', '16:10:00'),
(171, 'Jueves', '16:20:00'),
(172, 'Jueves', '16:30:00'),
(173, 'Jueves', '16:40:00'),
(174, 'Jueves', '16:50:00'),
(175, 'Jueves', '17:00:00'),
(176, 'Jueves', '17:10:00'),
(177, 'Jueves', '17:20:00'),
(178, 'Jueves', '17:30:00'),
(179, 'Jueves', '17:40:00'),
(180, 'Jueves', '17:50:00'),
(181, 'Jueves', '18:00:00'),
(182, 'Jueves', '18:10:00'),
(183, 'Jueves', '18:20:00'),
(184, 'Jueves', '18:30:00'),
(185, 'Jueves', '18:40:00'),
(186, 'Jueves', '18:50:00'),
(187, 'Jueves', '19:00:00'),
(188, 'Jueves', '19:10:00'),
(189, 'Jueves', '19:20:00'),
(190, 'Jueves', '19:30:00'),
(191, 'Jueves', '19:40:00'),
(192, 'Jueves', '19:50:00'),
(193, 'Viernes', '10:00:00'),
(194, 'Viernes', '10:10:00'),
(195, 'Viernes', '10:20:00'),
(196, 'Viernes', '10:30:00'),
(197, 'Viernes', '10:40:00'),
(198, 'Viernes', '10:50:00'),
(199, 'Viernes', '11:00:00'),
(200, 'Viernes', '11:10:00'),
(201, 'Viernes', '11:20:00'),
(202, 'Viernes', '11:30:00'),
(203, 'Viernes', '11:40:00'),
(204, 'Viernes', '11:50:00'),
(205, 'Viernes', '12:00:00'),
(206, 'Viernes', '12:10:00'),
(207, 'Viernes', '12:20:00'),
(208, 'Viernes', '12:30:00'),
(209, 'Viernes', '12:40:00'),
(210, 'Viernes', '12:50:00'),
(211, 'Viernes', '13:00:00'),
(212, 'Viernes', '13:10:00'),
(213, 'Viernes', '13:20:00'),
(214, 'Viernes', '13:30:00'),
(215, 'Viernes', '13:40:00'),
(216, 'Viernes', '13:50:00'),
(217, 'Viernes', '16:00:00'),
(218, 'Viernes', '16:10:00'),
(219, 'Viernes', '16:20:00'),
(220, 'Viernes', '16:30:00'),
(221, 'Viernes', '16:40:00'),
(222, 'Viernes', '16:50:00'),
(223, 'Viernes', '17:00:00'),
(224, 'Viernes', '17:10:00'),
(225, 'Viernes', '17:20:00'),
(226, 'Viernes', '17:30:00'),
(227, 'Viernes', '17:40:00'),
(228, 'Viernes', '17:50:00'),
(229, 'Viernes', '18:00:00'),
(230, 'Viernes', '18:10:00'),
(231, 'Viernes', '18:20:00'),
(232, 'Viernes', '18:30:00'),
(233, 'Viernes', '18:40:00'),
(234, 'Viernes', '18:50:00'),
(235, 'Viernes', '19:00:00'),
(236, 'Viernes', '19:10:00'),
(237, 'Viernes', '19:20:00'),
(238, 'Viernes', '19:30:00'),
(239, 'Viernes', '19:40:00'),
(240, 'Viernes', '19:50:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ingresos`
--

CREATE TABLE `ingresos` (
  `id_ingreso` int(11) NOT NULL,
  `concepto` varchar(200) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL DEFAULT current_timestamp(),
  `id_admin` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pacientes`
--

CREATE TABLE `pacientes` (
  `id_paciente` int(11) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `dieta` varchar(200) NOT NULL,
  `peso` decimal(5,2) DEFAULT NULL,
  `id_admin` int(11) NOT NULL,
  `activo` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pacientes`
--

INSERT INTO `pacientes` (`id_paciente`, `nombre`, `dieta`, `peso`, `id_admin`, `activo`) VALUES
(1, 'asd', '123', 123.00, 1, 1),
(2, 'asdasd', 'asdasd', 999.99, 3, 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administrador`
--
ALTER TABLE `administrador`
  ADD PRIMARY KEY (`id_administrador`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `citas`
--
ALTER TABLE `citas`
  ADD PRIMARY KEY (`id_cita`),
  ADD UNIQUE KEY `unique_horario_fecha` (`id_horario`,`fecha`),
  ADD KEY `id_paciente` (`id_paciente`);

--
-- Indices de la tabla `horarios_disponibles`
--
ALTER TABLE `horarios_disponibles`
  ADD PRIMARY KEY (`id_horario`);

--
-- Indices de la tabla `ingresos`
--
ALTER TABLE `ingresos`
  ADD PRIMARY KEY (`id_ingreso`),
  ADD KEY `id_admin` (`id_admin`);

--
-- Indices de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  ADD PRIMARY KEY (`id_paciente`),
  ADD KEY `id_admin` (`id_admin`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administrador`
--
ALTER TABLE `administrador`
  MODIFY `id_administrador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `citas`
--
ALTER TABLE `citas`
  MODIFY `id_cita` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `horarios_disponibles`
--
ALTER TABLE `horarios_disponibles`
  MODIFY `id_horario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=241;

--
-- AUTO_INCREMENT de la tabla `ingresos`
--
ALTER TABLE `ingresos`
  MODIFY `id_ingreso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  MODIFY `id_paciente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `pacientes` (`id_paciente`) ON UPDATE CASCADE,
  ADD CONSTRAINT `citas_ibfk_2` FOREIGN KEY (`id_horario`) REFERENCES `horarios_disponibles` (`id_horario`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `ingresos`
--
ALTER TABLE `ingresos`
  ADD CONSTRAINT `ingresos_ibfk_1` FOREIGN KEY (`id_admin`) REFERENCES `administrador` (`id_administrador`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `pacientes`
--
ALTER TABLE `pacientes`
  ADD CONSTRAINT `pacientes_ibfk_1` FOREIGN KEY (`id_admin`) REFERENCES `administrador` (`id_administrador`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
