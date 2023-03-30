use std::fs;
use std::io;
use std::path::Path;
use std::fs::File;
use std::io::prelude::*;

fn get_all_paths(root_dir: &Path) -> io::Result<Vec<String>> {
    let mut paths = Vec::new();
    for entry in fs::read_dir(root_dir)? { //tuna error :(
        let entry = entry?;
        let path = entry.path();
        if path.is_dir() {
            match get_all_paths(&path) {
                Ok(child_paths) => paths.extend(child_paths),
                Err(e) if e.kind() == io::ErrorKind::PermissionDenied => {
                    // Handle the permission denied error here
                    eprintln!("Permission denied for directory: {}, {}", path.display(), &e);
                },
                Err(e) => return Err(e),
            }
        } else {
            paths.push(path.to_string_lossy().to_string());
        }
    }
    Ok(paths)
}


fn main() -> io::Result<()> {
    let root_dir = "C:/";
    let paths = get_all_paths(Path::new(root_dir))?;
    let mut file = File::create("paths.txt")?;
    for path in paths {
        let message = writeln!(file, "{}", path).expect("Failed to write");
    }
    Ok(())
}