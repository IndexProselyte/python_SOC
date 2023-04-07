use std::fs;
use std::io;
use std::path::Path;
use std::fs::File;
use std::io::{BufWriter, Write};

fn safe_check(str_path: &String)-> bool{
    let allowed_dirs = ["Documents", "Games", "User", "Pictures", "Downloads", "Desktop", "Videos", "Music", "Program Files", "Users", "Program Files (x86)"];
    for word in allowed_dirs{
        if str_path.contains(word){
            return true
        }
    }
    return false
}

fn get_all_paths(root_dir: &Path) -> io::Result<Vec<String>> {
    let mut paths = Vec::new();
    for entry in fs::read_dir(root_dir)? { // Read root directory from which you continue inwards
        let entry = entry?; //is using the question mark operator to handle a potential error that could arise when trying to unwrap an Option type stored in the "entry" 
        let path = entry.path();
        let str_path = path.clone().into_os_string().into_string().unwrap();
        let is_ok = safe_check(&str_path);
        if is_ok == true{
            if path.is_dir() {  
                    match get_all_paths(&path) {
                        Ok(child_paths) => paths.extend(child_paths), // push directory paths 
                        Err(e) if e.kind() == io::ErrorKind::PermissionDenied => {
                            eprintln!("");
                        },
                        Err(e) => return Err(e),
                    }
                }
        } else {paths.push(path.to_string_lossy().to_string());} // push filepaths
    }
    Ok(paths)
}
// Add more drives
fn main() -> io::Result<()> {
    let root_dir = "C:/";
    let paths = get_all_paths(Path::new(root_dir))?;
    let mut file = BufWriter::with_capacity(20_00,File::create("output.txt").unwrap());
    for path in paths {
        writeln!(file, "{}", path).expect("Failed to write");
    }
    Ok(())
}