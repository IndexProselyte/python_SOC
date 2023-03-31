use std::fs;
use std::io;
use std::path::Path;
use std::fs::File;
use std::io::prelude::*;


fn safe_check(str_path: String)-> bool{
    let banned_dirs = ["Windows","System32","Temp"];
    for word in banned_dirs{
        if str_path.contains(word){
            return false
        }
    }
    return true
}

fn print_type_of<T>(_: &T) {
    println!("{}", std::any::type_name::<T>())
}
fn get_all_paths(root_dir: &Path) -> io::Result<Vec<String>> {
    let mut paths = Vec::new();
    for entry in fs::read_dir(root_dir)? { // Read root directory from which you continue inwards
        let entry = entry?; //is using the question mark operator to handle a potential error that could arise when trying to unwrap an Option type stored in the "entry" 
        let path = entry.path();
        let str_path = path.clone().into_os_string().into_string().unwrap();
        let is_ok = safe_check(str_path);
        //print_type_of(&path);
        if path.is_dir() {  
            if is_ok == true{
                match get_all_paths(&path) {
                    Ok(child_paths) => paths.extend(child_paths),
                    Err(e) if e.kind() == io::ErrorKind::PermissionDenied => {
                        // Handle the permission denied error here
                        eprintln!("Permission denied for directory: {}, {}", path.display(), &e);
                    },
                    Err(e) => return Err(e),
                }
            }

        } else {paths.push(path.to_string_lossy().to_string());}
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