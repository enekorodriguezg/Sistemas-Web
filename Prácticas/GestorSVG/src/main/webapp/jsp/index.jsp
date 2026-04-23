<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>
<!DOCTYPE html>
<html lang="es">
<head>
	<title>Gestor SVG</title>
	<%-- Ruta absoluta para el CSS --%>
	<link href="<%= request.getContextPath() %>/css/styleSheet.css" rel="stylesheet">
	<meta charset="utf-8">
</head>

<body>
<header>
	<h1>Gestor de imágenes SVG en base de datos eXist</h1>
	<h2>Sistemas Web 2026</h2>
</header>

<% if (request.getAttribute("informacion") != null) { %>
<section class="info-box">
	<strong>Información:</strong>
	<%= request.getAttribute("informacion") %>
</section>
<% } %>

<%-- 1. LISTAR RECURSOS (Usa GET porque es una lectura) --%>
<section>
	<table>
		<tr>
			<td class="aside-label"><h4>Mostrar las imágenes SVG de una colección</h4></td>
			<td class="form-container">
				<form id="LeerRecursos" method="GET" action="<%= request.getContextPath() %>/apiLR">
					<table>
						<tr>
							<td>Introducir nombre de la colección:</td>
							<td><input required name="collection"></td>
						</tr>
					</table>
					<hr>
					<button type="submit">Ver imágenes</button>
				</form>
			</td>
		</tr>
	</table>
</section>

<%-- 2. CREAR COLECCIÓN (Usa POST porque modifica la DB) --%>
<section>
	<table>
		<tr>
			<td class="aside-label"><h4>Crear una nueva colección de imágenes SVG</h4></td>
			<td class="form-container">
				<form id="CrearColeccion" method="POST" action="<%= request.getContextPath() %>/apiCC">
					<table>
						<tr>
							<td>Introducir nombre de la colección:</td>
							<td><input required name="collection"></td>
						</tr>
					</table>
					<hr>
					<button type="submit">Crear colección</button>
				</form>
			</td>
		</tr>
	</table>
</section>

<%-- 3. NUEVA IMAGEN BLANCO (Usa POST) --%>
<section>
	<table>
		<tr>
			<td class="aside-label"><h4>Crear una nueva imagen SVG (en blanco)</h4></td>
			<td class="form-container">
				<form id="ImagenNueva" method="POST" action="<%= request.getContextPath() %>/apiNI">
					<table>
						<tr>
							<td>Nombre de la nueva imagen SVG:</td>
							<td><input required name="svgName" placeholder="ejemplo.svg"></td>
						</tr>
						<tr>
							<td>Colección destino:</td>
							<td><input required name="collection"></td>
						</tr>
					</table>
					<hr>
					<button type="submit">Nueva imagen</button>
				</form>
			</td>
		</tr>
	</table>
</section>

<%-- 4. BORRAR COLECCIÓN (Usa POST) --%>
<section>
	<table>
		<tr>
			<td class="aside-label"><h4>Borrar una colección de imágenes SVG</h4></td>
			<td class="form-container">
				<form id="BorrarColeccion" method="POST" action="<%= request.getContextPath() %>/apiDC">
					<table>
						<tr>
							<td>Introducir nombre de la colección:</td>
							<td><input required name="collection"></td>
						</tr>
					</table>
					<hr>
					<button type="submit" class="btn-danger">Borrar colección</button>
				</form>
			</td>
		</tr>
	</table>
</section>

<%-- 5. SUBIR ARCHIVO (Usa POST y JavaScript) --%>
<section>
	<table>
		<tr>
			<td class="aside-label"><h4>Sube una imagen SVG desde un archivo local</h4></td>
			<td class="form-container">
				<input type="file" id="fileInput" accept=".svg">
				<button type="button" onclick="leerArchivo()">Leer Archivo</button>
				<hr>
				<form id="ImagenFichero" method="POST" action="<%= request.getContextPath() %>/apiNIF">
					<input type="hidden" id="contenidoArchivo" name="imagenSVG">
					<table>
						<tr>
							<td>Nombre de la imagen:</td>
							<td><input id="nombreArchivo" required name="svgName"></td>
						</tr>
						<tr>
							<td>Colección destino:</td>
							<td><input required name="collection"></td>
						</tr>
					</table>
					<hr>
					<button type="submit">Subir imagen</button>
				</form>
			</td>
		</tr>
	</table>
</section>

<footer><h5>Sistemas Web - Escuela Ingeniería de Bilbao - EHU</h5></footer>

<script>
	function leerArchivo() {
		var fileInput = document.getElementById('fileInput');
		var file = fileInput.files[0];
		if (!file) {
			alert('Por favor, selecciona un archivo primero.');
			return;
		}
		var reader = new FileReader();
		reader.onload = function(event) {
			document.getElementById('nombreArchivo').value = file.name;
			document.getElementById('contenidoArchivo').value = event.target.result;
			alert('Archivo leído correctamente. Ahora puedes pulsar "Subir imagen".');
		};
		reader.onerror = function() {
			alert("Error al leer el archivo.");
		};
		reader.readAsText(file);
	}
</script>
</body>
</html>