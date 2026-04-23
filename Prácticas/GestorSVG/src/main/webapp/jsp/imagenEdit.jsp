<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8" %>
<%@ page import="java.util.*" %>
<%
	response.setHeader("Cache-Control", "no-cache, no-store, must-revalidate");
	response.setHeader("Pragma", "no-cache");
	response.setDateHeader("Expires", 0);

	String collection = (String) request.getAttribute("collection");
	String svgName = (String) request.getAttribute("svgName");
	String imagenSVG = (String) request.getAttribute("imagenSVG");
	String imagenURI = (String) request.getAttribute("imagenURI") + "?nocache=" + new java.util.Date().getTime();
%>
<!DOCTYPE html>
<html lang="es">
<head>
	<meta charset="utf-8">
	<title>Edición SVG - <%=svgName%></title>
	<link href="<%= request.getContextPath() %>/css/styleSheet.css" rel="stylesheet">
</head>
<body>
<header>
	<h1>Gestor Imágenes SVG en eXist - SW-2026</h1>
	<h3>Edición de la imagen: <%=svgName%></h3>
</header>

<nav class="menu">
	<a href="<%= request.getContextPath() %>/jsp/index.jsp"> Inicio </a>
	<a href="javascript:void(0);" onclick="document.getElementById('backform').submit();">Atrás</a>
</nav>

<form id="backform" method="GET" action="<%= request.getContextPath() %>/apiLR">
	<input type="hidden" name="collection" value="<%=collection%>" />
</form>

<table style="width:100%" class="edicion">
	<tr class="edicion">
		<th class="edicion">Imagen Original</th>
		<th class="edicion">Imagen Modificada (Vista Previa)</th>
		<th class="edicion">SRC (Código Fuente)</th>
	</tr>
	<tr class="edicion">
		<td class="edicion">
			<object class="edicion" data="<%=imagenURI%>" type="image/svg+xml"></object>
		</td>
		<td class="edicion">
			<%-- Contenedor donde JavaScript inyectará el SVG modificado --%>
			<div id="previewSVG">
				<%=imagenSVG%>
			</div>
		</td>
		<td class="edicion">
			<form id="formulario" method="POST" action="<%= request.getContextPath() %>/appSaveUpdate">
				<input type="hidden" name="collection" value="<%=collection%>" />
				<input type="hidden" name="svgName" value="<%=svgName%>" />
				<%-- He añadido el id="textareaSVG" para que JS lo encuentre --%>
				<textarea class="input-field" name="imagenSVG" wrap="soft" id="textareaSVG"
						  rows="20" cols="80"><%=imagenSVG%></textarea>
			</form>
		</td>
	</tr>
</table>

<nav class="menu">
	<label for="opciones"></label>
	<select id="opciones" name="actualizar_salva" form="formulario">
		<option value="update">Actualizar</option>
		<option value="save">Guardar como copia</option>
	</select>
	<button type="submit" form="formulario">Actualizar/Guardar</button>
</nav>

<footer><h5>Sistemas Web - Escuela Ingeniería de Bilbao - EHU</h5></footer>

<script>
	const editor = document.getElementById('textareaSVG');
	const vistaPrevia = document.getElementById('previewSVG');

	// Escuchamos cada vez que el usuario teclea (input)
	editor.addEventListener('input', function() {
		vistaPrevia.innerHTML = this.value;
	});
</script>
</body>
</html>