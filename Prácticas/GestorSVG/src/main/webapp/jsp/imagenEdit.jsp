<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8" %>
<%@ page import="java.util.*" %>
<%
	// 1. CONTROL DE CACHÉ (Nivel Servidor)
	// Esto evita los errores "Wrong attribute value" que te daba el IDE
	response.setHeader("Cache-Control", "no-cache, no-store, must-revalidate");
	response.setHeader("Pragma", "no-cache");
	response.setDateHeader("Expires", 0);

	// 2. CAPTURA DE ATRIBUTOS ENVIADOS POR EL SERVLET
	String collection = (String) request.getAttribute("collection");
	String svgName = (String) request.getAttribute("svgName");
	String imagenSVG = (String) request.getAttribute("imagenSVG");
	String imagenURI = (String) request.getAttribute("imagenURI");

	// 3. GENERACIÓN DE TIMESTAMP (Evitamos 'System' por el error de compilación)
	// Usamos new Date().getTime() que es equivalente
	long timestamp = new java.util.Date().getTime();
	String uriFinal = (imagenURI != null) ? imagenURI + "?v=" + timestamp : "";
%>
<!DOCTYPE html>
<html lang="es">
<head>
	<meta charset="utf-8">
	<title>Edición SVG: <%= svgName %></title>
	<%-- CSS con ruta absoluta para evitar errores de carga --%>
	<link href="<%= request.getContextPath() %>/css/styleSheet.css" rel="stylesheet">
</head>
<body>
<header>
	<h1>Gestor Imágenes SVG en eXist - SW-2026</h1>
	<h3>Edición de la imagen: <%= svgName %></h3>
</header>

<nav class="menu">
	<%-- Enlace a inicio --%>
	<a href="<%= request.getContextPath() %>/jsp/index.jsp"> Inicio </a>

	<%-- Volver a la lista usando GET para evitar el error 405 --%>
	<a href="javascript:void(0);" onclick="document.getElementById('backform').submit();" style="color:white; text-decoration:underline;">Volver a la lista</a>
</nav>

<%-- Formulario oculto para navegar atrás --%>
<form id="backform" method="GET" action="<%= request.getContextPath() %>/apiLR">
	<input type="hidden" name="collection" value="<%= collection %>" />
</form>

<table style="width:100%" class="edicion">
	<tr class="edicion">
		<th class="edicion">Imagen Original</th>
		<th class="edicion">Código Fuente SVG (Editable)</th>
	</tr>
	<tr class="edicion">
		<td class="edicion">
			<%-- Visualización del SVG --%>
			<object class="edicion" data="<%= uriFinal %>" type="image/svg+xml" style="min-height:300px; width:100%; border:1px solid #444;">
				Su navegador no soporta visualización de SVG.
			</object>
		</td>
		<td class="edicion">
			<%-- Formulario para guardar cambios --%>
			<form id="formulario" method="POST" action="<%= request.getContextPath() %>/appSaveUpdate">
				<input type="hidden" name="collection" value="<%= collection %>" />
				<input type="hidden" name="svgName" value="<%= svgName %>" />
				<textarea class="input-field" name="imagenSVG" wrap="soft" rows="25" cols="80"
						  style="font-family:monospace; font-size:12px; background:#f4f4f4;"><%= imagenSVG %></textarea>
			</form>
		</td>
	</tr>
</table>

<nav class="menu">
	<label for="opciones">Acción:</label>
	<select id="opciones" name="actualizar_salva" form="formulario">
		<option value="update">Actualizar (Sobreescribir)</option>
		<option value="save">Guardar como copia</option>
	</select>
	<button type="submit" form="formulario">Guardar Cambios</button>
</nav>

<footer><h5>Sistemas Web - Escuela Ingeniería de Bilbao - EHU</h5></footer>
</body>
</html>