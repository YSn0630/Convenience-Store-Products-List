from PyQt5.QtWidgets import *
from convDB_connect import DB, config
import unicodedata


class Ins_lists(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DB(**config)
        self.setWindowTitle("상품 추가")

        central = QWidget()
        self.setCentralWidget(central)
        v_box = QVBoxLayout(central)

        self.input_name = QLineEdit()
        self.input_price = QLineEdit()
        self.input_EA = QSpinBox()
        self.input_EA.setRange(0,999)

        v_box.addWidget(QLabel("상품명"))
        v_box.addWidget(self.input_name)
        v_box.addWidget(QLabel("가격"))
        v_box.addWidget(self.input_price)
        v_box.addWidget(QLabel("재고 수량"))
        v_box.addWidget(self.input_EA)
        self.btn_yes = QPushButton("확인")
        self.btn_yes.clicked.connect(self.ins_lists)
        v_box.addWidget(self.btn_yes)

    def ins_lists(self):
        name = self.input_name.text().strip()
        price = self.input_price.text().strip()
        EA = self.input_EA.value()
        if not name or not price:
            QMessageBox.warning(self, "오류", "상품명과 가격을 모두 입력하세요.")
            return
        ok = self.db.insert_list(name, price, EA)
        if ok:
            QMessageBox.information(self, "완료", "추가되었습니다.")
            self.input_name.clear()
            self.input_price.clear()
            self.input_EA.clear()
        else:
            QMessageBox.critical(self, "실패", "추가 중 오류가 발생하였습니다.")

class Upd_lists(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DB(**config)
        self.setWindowTitle("상품 수정")

        central = QWidget()
        self.setCentralWidget(central)
        v_box = QVBoxLayout(central)

        v_box.addWidget(QLabel("발주코드(필수 기입)"))
        self.code = QLineEdit()
        v_box.addWidget(self.code)
        v_box.addWidget(QLabel("상품명(공란 시 미반영)"))
        self.name = QLineEdit()
        v_box.addWidget(self.name)
        v_box.addWidget(QLabel("가격(공란 시 미반영)"))
        self.price = QLineEdit()
        v_box.addWidget(self.price)
        v_box.addWidget(QLabel("운영재고"))
        self.EA = QSpinBox()
        self.EA.setRange(0,999)
        v_box.addWidget(self.EA)
        self.btn_yes = QPushButton("확인")
        self.btn_yes.clicked.connect(self.upd_lists)
        v_box.addWidget(self.btn_yes)

    def upd_lists(self):
        code = self.code.text().strip()
        if not code:
            QMessageBox.warning(self, "경고", "발주코드를 입력해 주십시오.")
            return

        result = self.db.find_list(code)
        
        if result == False:
            QMessageBox.warning(self, "오류", "검색된 데이터가 없습니다.")
            return
        else:
            name = self.name.text().strip()
            price = self.price.text().strip()
            EA = self.EA.value()

            ok = self.db.update_list(code, name, price, EA)

            if ok:
                QMessageBox.information(self, "완료", "수정되었습니다.")
                self.code.clear()
                self.name.clear()
                self.price.clear()
                self.EA.setValue(0)
            else:
                QMessageBox.critical(self, "실패", "수정 중 오류가 발생하였습니다.")

class Dlt_lists(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DB(**config)

        self.setWindowTitle("상품 제거")

        central = QWidget()
        self.setCentralWidget(central)
        v_box = QVBoxLayout(central)

        self.input_id_or_name = QLineEdit()

        v_box.addWidget(QLabel("발주코드 혹은 상품명 입력"))
        v_box.addWidget(self.input_id_or_name)
        self.btn_yes = QPushButton("확인")
        self.btn_yes.clicked.connect(self.dlt_lists)
        v_box.addWidget(self.btn_yes)

    def dlt_lists(self):
        id_or_name = self.input_id_or_name.text().strip()
        id_or_name = unicodedata.normalize('NFKC', id_or_name)

        if not id_or_name:
            QMessageBox.warning(self, "오류", "발주코드 혹은 상품명을 입력해주십시오.")
            return
        
        ok = self.db.verify_list(id_or_name, id_or_name)
        if ok:
            identify = self.db.delete_list(id_or_name)
            if identify:
                QMessageBox.information(self, "완료", "제거되었습니다.")
                self.input_id_or_name.clear()
            else:
                QMessageBox.critical(self, "실패", "오류가 발생하였습니다.")
        else:
            QMessageBox.critical(self, "실패", "존재하지 않는 상품입니다.")