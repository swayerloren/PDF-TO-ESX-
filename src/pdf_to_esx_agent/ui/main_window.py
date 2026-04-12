from __future__ import annotations

import logging
import os
from pathlib import Path
import queue
import threading
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD

    _DND_AVAILABLE = True
except ImportError:  # pragma: no cover - UI fallback
    DND_FILES = None
    TkinterDnD = None
    _DND_AVAILABLE = False

from pdf_to_esx_agent.core.conversion_service import ConversionError, ConversionResult, ConversionService, ProgressUpdate
from pdf_to_esx_agent.core.settings import AppSettings
from pdf_to_esx_agent.models.estimate import CanonicalEstimate, ValidationMessage


class MainWindow:
    def __init__(
        self,
        settings: AppSettings,
        conversion_service: ConversionService,
        *,
        logger: logging.Logger | None = None,
    ) -> None:
        self._settings = settings
        self._conversion_service = conversion_service
        self._logger = logger or logging.getLogger("pdf_to_esx_agent").getChild("ui")
        self._events: queue.Queue[tuple[str, object]] = queue.Queue()
        self._selected_files: list[Path] = []
        self._worker: threading.Thread | None = None

        self._root = self._create_root()
        self._root.title(settings.app_title)
        self._root.geometry("1280x860")
        self._root.minsize(1040, 760)

        self.output_dir_var = tk.StringVar(value=str(settings.default_output_dir))
        self.status_var = tk.StringVar(value="Select one or more insurance estimate PDFs to begin.")
        self.success_var = tk.StringVar(value="")
        self.summary_var = tk.StringVar(value="No conversion run yet.")
        self.progress_var = tk.IntVar(value=0)

        self._configure_style()
        self._build_ui()
        self._root.after(100, self._poll_events)

    def run(self) -> None:
        self._root.mainloop()

    def _create_root(self) -> tk.Tk:
        if _DND_AVAILABLE:
            return TkinterDnD.Tk()
        return tk.Tk()

    def _configure_style(self) -> None:
        self._root.configure(bg="#eef2f6")
        style = ttk.Style(self._root)
        style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI Semibold", 20), foreground="#14324a", background="#eef2f6")
        style.configure("Subheader.TLabel", font=("Segoe UI", 10), foreground="#516575", background="#eef2f6")
        style.configure("Panel.TLabelframe", background="#f8fbfd", borderwidth=1, relief="solid")
        style.configure("Panel.TLabelframe.Label", font=("Segoe UI Semibold", 10), foreground="#14324a", background="#f8fbfd")
        style.configure("Accent.TButton", font=("Segoe UI Semibold", 10), padding=(12, 8))
        style.configure("Status.TLabel", foreground="#14324a", background="#eef2f6")
        style.configure("Success.TLabel", foreground="#156c42", background="#eef2f6", font=("Segoe UI Semibold", 10))

    def _build_ui(self) -> None:
        container = ttk.Frame(self._root, padding=18)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=3)
        container.columnconfigure(1, weight=2)
        container.rowconfigure(2, weight=1)
        container.rowconfigure(3, weight=1)

        header = ttk.Frame(container)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text=self._settings.app_title, style="Header.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Upload estimate PDFs, normalize the extracted data, and export a deterministic ESX/XML package.",
            style="Subheader.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        upload_panel = ttk.LabelFrame(container, text="Estimate PDFs", style="Panel.TLabelframe", padding=14)
        upload_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 12))
        upload_panel.columnconfigure(0, weight=1)
        upload_panel.rowconfigure(2, weight=1)

        self.drop_zone = tk.Label(
            upload_panel,
            text="Drag and drop PDF files here\nor use Add PDFs",
            justify="center",
            bg="#ffffff",
            fg="#21445f",
            relief="ridge",
            bd=2,
            padx=18,
            pady=24,
            font=("Segoe UI Semibold", 11),
        )
        self.drop_zone.grid(row=0, column=0, sticky="ew")
        self.drop_zone.bind("<Button-1>", lambda _event: self._choose_files())
        self._configure_drag_and_drop(self.drop_zone)

        upload_buttons = ttk.Frame(upload_panel)
        upload_buttons.grid(row=1, column=0, sticky="ew", pady=(12, 12))
        upload_buttons.columnconfigure(3, weight=1)
        ttk.Button(upload_buttons, text="Add PDFs", command=self._choose_files).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(upload_buttons, text="Remove Selected", command=self._remove_selected_file).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(upload_buttons, text="Clear", command=self._clear_files).grid(row=0, column=2)

        file_list_frame = ttk.Frame(upload_panel)
        file_list_frame.grid(row=2, column=0, sticky="nsew")
        file_list_frame.columnconfigure(0, weight=1)
        file_list_frame.rowconfigure(0, weight=1)

        self.file_list = tk.Listbox(
            file_list_frame,
            selectmode=tk.EXTENDED,
            activestyle="none",
            bg="#ffffff",
            fg="#1d2b36",
            borderwidth=1,
            relief="solid",
            font=("Segoe UI", 10),
        )
        self.file_list.grid(row=0, column=0, sticky="nsew")
        self._configure_drag_and_drop(self.file_list)

        file_list_scroll = ttk.Scrollbar(file_list_frame, orient="vertical", command=self.file_list.yview)
        file_list_scroll.grid(row=0, column=1, sticky="ns")
        self.file_list.configure(yscrollcommand=file_list_scroll.set)

        output_panel = ttk.LabelFrame(container, text="Output And Convert", style="Panel.TLabelframe", padding=14)
        output_panel.grid(row=1, column=1, sticky="nsew")
        output_panel.columnconfigure(0, weight=1)

        self.state_banner = tk.Label(
            output_panel,
            text="Ready. Select files and convert.",
            anchor="w",
            justify="left",
            bg="#dce6ef",
            fg="#14324a",
            padx=10,
            pady=10,
            font=("Segoe UI Semibold", 10),
        )
        self.state_banner.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        folder_frame = ttk.Frame(output_panel)
        folder_frame.grid(row=1, column=0, sticky="ew")
        folder_frame.columnconfigure(0, weight=1)
        ttk.Label(folder_frame, text="Output folder").grid(row=0, column=0, sticky="w")
        folder_entry = ttk.Entry(folder_frame, textvariable=self.output_dir_var)
        folder_entry.grid(row=1, column=0, sticky="ew", pady=(6, 0))
        ttk.Button(folder_frame, text="Browse", command=self._choose_output_dir).grid(row=1, column=1, padx=(8, 0), pady=(6, 0))

        action_frame = ttk.Frame(output_panel)
        action_frame.grid(row=2, column=0, sticky="ew", pady=(18, 12))
        action_frame.columnconfigure(0, weight=1)
        self.convert_button = ttk.Button(
            action_frame,
            text="Convert To ESX",
            style="Accent.TButton",
            command=self._start_conversion,
        )
        self.convert_button.grid(row=0, column=0, sticky="ew")
        ttk.Button(action_frame, text="Open Output Folder", command=self._open_output_dir).grid(row=1, column=0, sticky="ew", pady=(8, 0))

        ttk.Label(output_panel, text="Progress").grid(row=3, column=0, sticky="w", pady=(8, 4))
        self.progressbar = ttk.Progressbar(output_panel, maximum=100, variable=self.progress_var)
        self.progressbar.grid(row=4, column=0, sticky="ew")

        ttk.Label(output_panel, textvariable=self.status_var, style="Status.TLabel", wraplength=360).grid(
            row=5, column=0, sticky="w", pady=(10, 4)
        )
        ttk.Label(output_panel, textvariable=self.success_var, style="Success.TLabel", wraplength=360).grid(
            row=6, column=0, sticky="w", pady=(4, 0)
        )
        ttk.Label(output_panel, textvariable=self.summary_var, style="Subheader.TLabel", wraplength=360).grid(
            row=7, column=0, sticky="w", pady=(8, 0)
        )

        preview_panel = ttk.LabelFrame(container, text="Extracted Estimate Preview", style="Panel.TLabelframe", padding=12)
        preview_panel.grid(row=2, column=0, sticky="nsew", padx=(0, 12), pady=(12, 12))
        preview_panel.columnconfigure(0, weight=1)
        preview_panel.rowconfigure(0, weight=1)
        self.preview_text = self._build_text_panel(preview_panel)
        self.preview_text.grid(row=0, column=0, sticky="nsew")

        validation_panel = ttk.LabelFrame(container, text="Validation And Errors", style="Panel.TLabelframe", padding=12)
        validation_panel.grid(row=2, column=1, sticky="nsew", pady=(12, 12))
        validation_panel.columnconfigure(0, weight=1)
        validation_panel.rowconfigure(0, weight=1)
        self.validation_text = self._build_text_panel(validation_panel)
        self.validation_text.grid(row=0, column=0, sticky="nsew")

        log_panel = ttk.LabelFrame(container, text="Status Log", style="Panel.TLabelframe", padding=12)
        log_panel.grid(row=3, column=0, columnspan=2, sticky="nsew")
        log_panel.columnconfigure(0, weight=1)
        log_panel.rowconfigure(0, weight=1)
        self.log_text = self._build_text_panel(log_panel)
        self.log_text.grid(row=0, column=0, sticky="nsew")

        self._set_text(self.preview_text, "No estimate parsed yet.")
        self._set_text(self.validation_text, "No validation messages yet.")
        dnd_message = "Drag-and-drop is enabled." if _DND_AVAILABLE else "Drag-and-drop unavailable. Use Add PDFs."
        self._append_log(dnd_message)

    def _build_text_panel(self, parent: ttk.LabelFrame) -> ScrolledText:
        text = ScrolledText(
            parent,
            wrap="word",
            bg="#ffffff",
            fg="#1d2b36",
            relief="solid",
            borderwidth=1,
            font=("Consolas", 10),
        )
        text.configure(state="disabled")
        return text

    def _configure_drag_and_drop(self, widget: tk.Widget) -> None:
        if not _DND_AVAILABLE or DND_FILES is None:
            return
        widget.drop_target_register(DND_FILES)
        widget.dnd_bind("<<Drop>>", self._handle_drop)

    def _choose_files(self) -> None:
        selected = filedialog.askopenfilenames(
            parent=self._root,
            title="Select insurance estimate PDFs",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        if selected:
            self._add_files([Path(path) for path in selected])

    def _choose_output_dir(self) -> None:
        selected = filedialog.askdirectory(parent=self._root, title="Select output folder")
        if selected:
            self.output_dir_var.set(selected)

    def _handle_drop(self, event: tk.Event) -> None:
        try:
            raw_paths = self._root.tk.splitlist(event.data)
        except tk.TclError:
            raw_paths = [event.data]
        self._add_files([Path(path) for path in raw_paths])

    def _add_files(self, paths: list[Path]) -> None:
        added_files = 0
        for path in paths:
            normalized = Path(path).expanduser()
            if normalized.suffix.lower() != ".pdf":
                self._append_validation_messages(
                    [ValidationMessage("warning", f"Skipped non-PDF file: {normalized.name}")]
                )
                continue
            if normalized not in self._selected_files:
                self._selected_files.append(normalized)
                added_files += 1

        self._selected_files.sort(key=lambda path: path.name.lower())
        self._refresh_file_list()
        if added_files:
            self.status_var.set(f"{len(self._selected_files)} PDF file(s) ready for conversion.")
            self._set_banner("ready", f"Ready to convert {len(self._selected_files)} PDF file(s).")
            self._append_log(f"Selected {added_files} new PDF file(s).")

    def _remove_selected_file(self) -> None:
        selected_indices = list(self.file_list.curselection())
        if not selected_indices:
            return
        for index in reversed(selected_indices):
            del self._selected_files[index]
        self._refresh_file_list()
        self.status_var.set(f"{len(self._selected_files)} PDF file(s) ready for conversion.")
        if self._selected_files:
            self._set_banner("ready", f"Ready to convert {len(self._selected_files)} PDF file(s).")
        else:
            self._set_banner("ready", "Ready. Select files and convert.")

    def _clear_files(self) -> None:
        self._selected_files.clear()
        self._refresh_file_list()
        self.status_var.set("Select one or more insurance estimate PDFs to begin.")
        self.success_var.set("")
        self.summary_var.set("No conversion run yet.")
        self._set_banner("ready", "Ready. Select files and convert.")
        self._set_text(self.preview_text, "No estimate parsed yet.")
        self._set_text(self.validation_text, "No validation messages yet.")

    def _refresh_file_list(self) -> None:
        self.file_list.delete(0, tk.END)
        for path in self._selected_files:
            self.file_list.insert(tk.END, str(path))

    def _start_conversion(self) -> None:
        if self._worker and self._worker.is_alive():
            return
        if not self._selected_files:
            messagebox.showerror(self._settings.app_title, "Select at least one PDF before converting.")
            return

        try:
            output_dir = self._validated_output_dir()
        except ConversionError as exc:
            self._handle_error({"message": str(exc), "traceback": ""})
            return

        self.progress_var.set(0)
        self.success_var.set("")
        self.summary_var.set("Conversion in progress.")
        self.status_var.set("Starting conversion.")
        self._set_text(self.validation_text, "No validation messages yet.")
        self._set_banner("running", f"Converting {len(self._selected_files)} PDF file(s)...")
        self._append_log(f"Starting conversion for {len(self._selected_files)} file(s).")
        self.convert_button.configure(state="disabled")

        selected_files = list(self._selected_files)
        self._worker = threading.Thread(
            target=self._run_conversion,
            args=(selected_files, output_dir),
            daemon=True,
        )
        self._worker.start()

    def _run_conversion(self, selected_files: list[Path], output_dir: Path) -> None:
        try:
            result = self._conversion_service.convert(
                selected_files,
                output_dir,
                progress_callback=self._queue_progress,
            )
        except ConversionError as exc:  # pragma: no cover - UI worker
            self._events.put(
                (
                    "error",
                    {
                        "message": str(exc),
                        "traceback": "",
                    },
                )
            )
            return
        except Exception as exc:  # pragma: no cover - UI worker
            self._logger.exception("Conversion failed.")
            self._events.put(
                (
                    "error",
                    {
                        "message": str(exc),
                        "traceback": traceback.format_exc(),
                    },
                )
            )
            return
        self._events.put(("done", result))

    def _queue_progress(self, update: ProgressUpdate) -> None:
        self._events.put(("progress", update))

    def _poll_events(self) -> None:
        try:
            while True:
                event_type, payload = self._events.get_nowait()
                if event_type == "progress":
                    self._handle_progress(payload)
                elif event_type == "done":
                    self._handle_success(payload)
                elif event_type == "error":
                    self._handle_error(payload)
        except queue.Empty:
            pass
        self._root.after(100, self._poll_events)

    def _handle_progress(self, update: ProgressUpdate) -> None:
        self.progress_var.set(update.percent)
        self.status_var.set(update.message)
        self._set_banner("running", f"{update.message} ({update.percent}%)")
        self._append_log(update.message)

    def _handle_success(self, result: ConversionResult) -> None:
        self.convert_button.configure(state="normal")
        self.progress_var.set(100)
        warning_count = sum(1 for message in result.validation_messages if message.level != "info")
        self.status_var.set("Conversion complete." if warning_count == 0 else "Conversion complete with warnings.")
        self.success_var.set(f"Generated ESX package: {result.export_paths.esx_path}")
        self.summary_var.set(self._result_summary_text(result))
        self._set_text(self.preview_text, self._preview_text(result.canonical_estimate))
        self._append_validation_messages(result.validation_messages)
        if warning_count:
            self._set_banner("warning", f"ESX package created with {warning_count} warning(s). Review the validation panel.")
        else:
            self._set_banner("success", "ESX package created successfully.")
        self._append_log(f"XML written to {result.export_paths.xml_path}")
        self._append_log(f"ESX package written to {result.export_paths.esx_path}")
        self._append_log(f"Canonical JSON written to {result.export_paths.canonical_json_path}")
        messagebox.showinfo(
            self._settings.app_title,
            f"ESX package created successfully.\n\n{result.export_paths.esx_path}",
        )

    def _handle_error(self, payload: object) -> None:
        self.convert_button.configure(state="normal")
        self.progress_var.set(0)
        message = "Conversion failed."
        trace = ""
        if isinstance(payload, dict):
            message = str(payload.get("message") or message)
            trace = str(payload.get("traceback") or "")
        self.status_var.set(message)
        self.success_var.set("")
        self.summary_var.set("No export was written.")
        self._set_banner("error", "Conversion failed. Review the validation panel and log below.")
        self._append_log(message)
        validation_messages = [ValidationMessage("error", message)]
        if trace:
            self._append_log(trace)
            validation_messages.append(
                ValidationMessage("info", "Full stack trace was written to logs/pdf_to_esx_agent.log.")
            )
        self._append_validation_messages(validation_messages)
        messagebox.showerror(self._settings.app_title, message)

    def _open_output_dir(self) -> None:
        try:
            path = self._validated_output_dir()
        except ConversionError as exc:
            messagebox.showerror(self._settings.app_title, str(exc))
            return
        if os.name == "nt":
            os.startfile(path)  # type: ignore[attr-defined]
            return
        messagebox.showinfo(self._settings.app_title, str(path))

    def _validated_output_dir(self) -> Path:
        raw_value = self.output_dir_var.get().strip()
        path = Path(raw_value).expanduser() if raw_value else self._settings.default_output_dir
        resolved = path.resolve()
        if resolved.exists() and not resolved.is_dir():
            raise ConversionError(f"Selected output path is not a folder: {resolved}")
        try:
            resolved.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise ConversionError(f"Could not create or access the output folder: {resolved}") from exc
        self.output_dir_var.set(str(resolved))
        return resolved

    def _append_validation_messages(self, messages: list[ValidationMessage]) -> None:
        if not messages:
            self._set_text(self.validation_text, "No validation messages.")
            return
        lines = []
        for message in messages:
            context = f" [{message.context}]" if message.context else ""
            lines.append(f"{message.level.upper()}{context}: {message.message}")
        self._set_text(self.validation_text, "\n".join(lines))

    def _preview_text(self, estimate: CanonicalEstimate) -> str:
        summary = estimate.preview_summary()
        lines = [
            "Summary",
            f"Carrier: {summary['carrier']}",
            f"Insured: {summary['insured']}",
            f"Claim Number: {summary['claim_number']}",
            f"Estimate Number: {summary['estimate_number']}",
            f"Property: {summary['property_address']}",
            f"Line Items: {summary['line_item_count']}",
            f"Grand Total: {summary['grand_total']}",
            f"RCV: {summary['rcv']}",
            f"ACV: {summary['acv']}",
            f"Net Payable: {summary['net_payable']}",
            f"Deductible: {summary['deductible']}",
            f"Scan Modes: {summary['scan_modes']}",
            "",
            "First Line Items",
        ]
        if not estimate.line_items:
            lines.append("No line items parsed.")
        else:
            for index, item in enumerate(estimate.line_items[:15], start=1):
                quantity = "" if item.quantity is None else f"{item.quantity:g}"
                unit = item.unit or ""
                rcv = "" if item.replacement_cost is None else f"{item.replacement_cost:,.2f}"
                lines.append(
                    f"{index:02d}. {item.section_name or 'General'} | {quantity} {unit} | {item.description} | {rcv}"
                )
            if len(estimate.line_items) > 15:
                lines.append(f"... {len(estimate.line_items) - 15} more line item(s)")
        return "\n".join(lines)

    def _result_summary_text(self, result: ConversionResult) -> str:
        estimate = result.canonical_estimate
        ocr_pages = sum(source.ocr_page_count for source in estimate.source_documents)
        warning_count = sum(1 for message in result.validation_messages if message.level != "info")
        return (
            f"Files: {len(estimate.source_documents)} | "
            f"Line items: {len(estimate.line_items)} | "
            f"Warnings: {warning_count} | "
            f"OCR pages used: {ocr_pages}"
        )

    def _set_banner(self, kind: str, text: str) -> None:
        palette = {
            "ready": ("#dce6ef", "#14324a"),
            "running": ("#d6ecff", "#0d4e7a"),
            "success": ("#d8f3e6", "#156c42"),
            "warning": ("#fff1cf", "#8a5a00"),
            "error": ("#ffe0dd", "#a12622"),
        }
        background, foreground = palette.get(kind, palette["ready"])
        self.state_banner.configure(text=text, bg=background, fg=foreground)

    def _set_text(self, widget: ScrolledText, value: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", value.strip())
        widget.configure(state="disabled")

    def _append_log(self, value: str) -> None:
        widget = self.log_text
        widget.configure(state="normal")
        widget.insert(tk.END, value.rstrip() + "\n")
        widget.see(tk.END)
        widget.configure(state="disabled")
