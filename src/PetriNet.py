import numpy as np
import xml.etree.ElementTree as ET # new lib
from typing import List, Optional

class PetriNet:
    def __init__(
        self,
        place_ids: List[str],
        trans_ids: List[str],
        place_names: List[Optional[str]],
        trans_names: List[Optional[str]],
        I: np.ndarray,   
        O: np.ndarray, 
        M0: np.ndarray
    ):
        self.place_ids = place_ids
        self.trans_ids = trans_ids
        self.place_names = place_names
        self.trans_names = trans_names
        self.I = I
        self.O = O
        self.M0 = M0

    @classmethod
    def from_pnml(cls, filename: str) -> "PetriNet":
        tree = ET.parse(filename)
        root = tree.getroot()

        # Namespace PNML
        ns = {"pnml": "http://www.pnml.org/version-2009/grammar/pnml"}

        # Tìm <net>
        net = root.find("pnml:net", ns)
        page = net.find("pnml:page", ns)

        # --- Parse places ---
        place_ids = []
        place_names = []
        initial_marking = []

        for pl in page.findall("pnml:place", ns):
            pid = pl.get("id")
            place_ids.append(pid)

            name_tag = pl.find("pnml:name/pnml:text", ns)
            place_names.append(name_tag.text if name_tag is not None else None)

            # marking ban đầu
            im_tag = pl.find("pnml:initialMarking/pnml:text", ns)
            m0 = int(im_tag.text) if im_tag is not None else 0
            initial_marking.append(m0)

        # --- Parse transitions ---
        trans_ids = []
        trans_names = []

        for tr in page.findall("pnml:transition", ns):
            tid = tr.get("id")
            trans_ids.append(tid)

            name_tag = tr.find("pnml:name/pnml:text", ns)
            trans_names.append(name_tag.text if name_tag is not None else None)

        # --- Tạo index mapping ---
        p_index = {pid: i for i, pid in enumerate(place_ids)}
        t_index = {tid: j for j, tid in enumerate(trans_ids)}

        # Ma trận I và O
        I = np.zeros((len(trans_ids), len(place_ids)), dtype=int)
        O = np.zeros((len(trans_ids), len(place_ids)), dtype=int)

        # --- Parse arcs ---
        for arc in page.findall("pnml:arc", ns):
            source = arc.get("source")
            target = arc.get("target")

            # place → transition  => input arc => I[place, trans] += 1
            if source in p_index and target in t_index:
                I[t_index[target], p_index[source]] += 1

            # transition → place  => output arc => O[place, trans] += 1
            if source in t_index and target in p_index:
                O[t_index[source], p_index[target]] += 1

        M0 = np.array(initial_marking, dtype=int)

        return cls(
            place_ids=place_ids,
            trans_ids=trans_ids,
            place_names=place_names,
            trans_names=trans_names,
            I=I,
            O=O,
            M0=M0
        )

    def validate(self, strict: bool = True):
        """
        Kiểm tra tính nhất quán của mạng Petri.
        strict=True  → ném exception nếu có lỗi
        strict=False → in cảnh báo
        """

        errors = []
        warnings = []

        # 1. kiểm tra có place/trans không
        if len(self.place_ids) == 0:
            errors.append("No places found in PNML.")
        if len(self.trans_ids) == 0:
            errors.append("No transitions found in PNML.")

        # 2. ID trùng
        if len(self.place_ids) != len(set(self.place_ids)):
            errors.append("Duplicate place IDs detected.")
        if len(self.trans_ids) != len(set(self.trans_ids)):
            errors.append("Duplicate transition IDs detected.")

        # 3. marking âm
        for i, m in enumerate(self.M0):
            if m < 0:
                errors.append(f"Place '{self.place_ids[i]}' has negative marking {m}.")

        # 4. kiểm tra kích thước I/O
        t_count = len(self.trans_ids)
        p_count = len(self.place_ids)

        if self.I.shape != (t_count, p_count):
            errors.append(f"I matrix size mismatch. Expected {(t_count, p_count)}, got {self.I.shape}.")
        if self.O.shape != (t_count, p_count):
            errors.append(f"O matrix size mismatch. Expected {(t_count, p_count)}, got {self.O.shape}.")

        # 5. transition không có input/output
        for ti, tid in enumerate(self.trans_ids):
            if np.all(self.I[ti] == 0) and np.all(self.O[ti] == 0):
                warnings.append(f"Transition '{tid}' is isolated (no input nor output arcs).")

        # 6. place cô lập
        for pi, pid in enumerate(self.place_ids):
            if np.all(self.I[:, pi] == 0) and np.all(self.O[:, pi] == 0):
                warnings.append(f"Place '{pid}' is isolated (no arcs).")

        # ---------------------------------------------------------
        # Xử lý kết quả
        # ---------------------------------------------------------
        if errors and strict:
            raise ValueError(
                "PetriNet validation failed:\n" +
                "\n".join(" - " + e for e in errors)
            )

        if strict:
            if warnings:
                print("Validation warnings:")
                for w in warnings:
                    print(" -", w)
        else:
            for e in errors:
                print("[ERROR]", e)
            for w in warnings:
                print("[WARN]", w)
                

    def __str__(self) -> str:
        s = []
        s.append("Places: " + str(self.place_ids))
        s.append("Place names: " + str(self.place_names))
        s.append("\nTransitions: " + str(self.trans_ids))
        s.append("Transition names: " + str(self.trans_names))
        s.append("\nI (input) matrix:")
        s.append(str(self.I))
        s.append("\nO (output) matrix:")
        s.append(str(self.O))
        s.append("\nInitial marking M0:")
        s.append(str(self.M0))
        return "\n".join(s)
