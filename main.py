import sys
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QMainWindow,
    QMessageBox, QTableWidgetItem
)
from ui_bugtracker import Ui_VentanaPrincipal
import bd


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_VentanaPrincipal()
        self.ui.setupUi(self)

        self.ui.btnAnadir.clicked.connect(self.anadir_incidencia)
        self.ui.btnModificar.clicked.connect(self.modificar_incidencia)
        self.ui.btnEliminar.clicked.connect(self.eliminar_incidencia)
        self.ui.btnLimpiar.clicked.connect(self.limpiar_formulario)
        self.ui.tblIncidencias.itemSelectionChanged.connect(self.cargar_seleccion)

        self.cargar_incidencias()
        self.actualizar_botones()

    def cargar_incidencias(self):
        try:
            incidencias = bd.obtener_incidencias()
        except sqlite3.Error:
            QMessageBox.critical(
                self,
                "Error",
                "No se han podido cargar las incidencias."
            )
            return

        tabla = self.ui.tblIncidencias
        tabla.setRowCount(0)

        for incidencia in incidencias:
            fila = tabla.rowCount()
            tabla.insertRow(fila)

            tabla.setItem(fila, 0, QTableWidgetItem(str(incidencia["id"])))
            tabla.setItem(fila, 1, QTableWidgetItem(incidencia["titulo"]))
            tabla.setItem(fila, 2, QTableWidgetItem(incidencia["tipo"]))
            tabla.setItem(fila, 3, QTableWidgetItem(incidencia["prioridad"]))
            tabla.setItem(fila, 4, QTableWidgetItem(incidencia["estado"]))

        tabla.setColumnHidden(0, True)
        tabla.clearSelection()
        self.actualizar_botones()

    def actualizar_botones(self):
        hay_seleccion = bool(self.ui.tblIncidencias.selectedItems())
        self.ui.btnModificar.setEnabled(hay_seleccion)
        self.ui.btnEliminar.setEnabled(hay_seleccion)

    def cargar_seleccion(self):
        items = self.ui.tblIncidencias.selectedItems()

    # Si no hay selección, solo se actualizan los botones
        if not items:
            self.actualizar_botones()
            return

        fila = items[0].row()
        id_incidencia = int(self.ui.tblIncidencias.item(fila, 0).text())

        try:
            incidencia = bd.obtener_incidencia(id_incidencia)
        except sqlite3.Error:
            QMessageBox.critical(
                self,
                "Error",
                "No se ha podido cargar la incidencia seleccionada."
            )
            return

    # Si la incidencia ya no existe, no se rellena el formulario
        if incidencia is None:
            self.ui.tblIncidencias.clearSelection()
            self.actualizar_botones()
            return

        self.ui.txtTitulo.setText(incidencia["titulo"])
        self.ui.cmbTipo.setCurrentText(incidencia["tipo"])
        self.ui.cmbPrioridad.setCurrentText(incidencia["prioridad"])
        self.ui.cmbEstado.setCurrentText(incidencia["estado"])
        self.ui.txtDescripcion.setPlainText(incidencia["descripcion"])

        self.actualizar_botones()

    def anadir_incidencia(self):
        pass

    def modificar_incidencia(self):
        pass

    def eliminar_incidencia(self):
        pass

    def limpiar_formulario(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        bd.crear_bd()
    except sqlite3.Error:
        QMessageBox.critical(None, "Error", "No se ha podido preparar la base de datos.")
        sys.exit(1)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())