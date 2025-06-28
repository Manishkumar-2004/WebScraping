import base64
import os

def drop_file(driver, drop_target, file_path, logger):
    file_path = os.path.abspath(file_path)
    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        content = f.read()

    b64_content = base64.b64encode(content).decode()

    driver.execute_script(
        """
        var b64contents = arguments[0];
        var fileName = arguments[1];
        var target = arguments[2];

        function b64ToUint8Array(b64) {
            var binary_string = window.atob(b64);
            var len = binary_string.length;
            var bytes = new Uint8Array(len);
            for (var i = 0; i < len; i++) {
                bytes[i] = binary_string.charCodeAt(i);
            }
            return bytes;
        }

        var uint8Array = b64ToUint8Array(b64contents);
        var blob = new Blob([uint8Array], {type: 'image/jpeg'});
        var file = new File([blob], fileName, {type: 'image/jpeg'});

        var dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);

        var event = new DragEvent('drop', {
            dataTransfer: dataTransfer,
            bubbles: true,
            cancelable: true
        });

        target.dispatchEvent(event);
        """,
        b64_content,
        file_name,
        drop_target
    )
    logger.info(f"File {file_name} dropped successfully")
