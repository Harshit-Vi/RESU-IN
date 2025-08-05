import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { FileText, Upload, X, AlertCircle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  acceptedTypes: string[];
  maxSize: number;
  label: string;
  description: string;
  selectedFile?: File | null;
}

export const FileUpload = ({
  onFileSelect,
  acceptedTypes,
  maxSize,
  label,
  description,
  selectedFile
}: FileUploadProps) => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const { toast } = useToast();

  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
    if (rejectedFiles.length > 0) {
      const error = rejectedFiles[0].errors[0];
      toast({
        title: "Upload Error",
        description: error.message,
        variant: "destructive",
      });
      return;
    }

    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      setIsUploading(true);
      setUploadProgress(0);

      // Simulate upload progress
      const interval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 100) {
            clearInterval(interval);
            setIsUploading(false);
            onFileSelect(file);
            toast({
              title: "Upload Successful",
              description: `${file.name} has been uploaded successfully.`,
            });
            return 100;
          }
          return prev + 10;
        });
      }, 100);
    }
  }, [onFileSelect, toast]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: acceptedTypes.reduce((acc, type) => ({ ...acc, [type]: [] }), {}),
    maxSize,
    multiple: false,
  });

  const removeFile = () => {
    onFileSelect(null as any);
    setUploadProgress(0);
    setIsUploading(false);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  if (selectedFile && !isUploading) {
    return (
      <Card className="p-6 border-dashed border-2 border-primary/20 bg-primary/5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
              <FileText className="w-5 h-5 text-primary" />
            </div>
            <div>
              <p className="font-medium">{selectedFile.name}</p>
              <p className="text-sm text-muted-foreground">
                {formatFileSize(selectedFile.size)}
              </p>
            </div>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={removeFile}
            className="hover:bg-destructive/10 hover:text-destructive"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>
      </Card>
    );
  }

  return (
    <Card className="p-6">
      <div className="space-y-4">
        <div>
          <h3 className="font-semibold text-lg">{label}</h3>
          <p className="text-muted-foreground text-sm">{description}</p>
        </div>

        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all duration-200
            ${isDragActive 
              ? 'border-primary bg-primary/5 scale-[1.02]' 
              : 'border-muted hover:border-primary/50 hover:bg-muted/50'
            }
          `}
        >
          <input {...getInputProps()} />
          
          <div className="space-y-4">
            <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mx-auto">
              <Upload className="w-6 h-6 text-primary" />
            </div>
            
            {isDragActive ? (
              <p className="text-primary font-medium">Drop your file here...</p>
            ) : (
              <div className="space-y-2">
                <p className="text-foreground font-medium">
                  Click to upload or drag and drop
                </p>
                <p className="text-muted-foreground text-sm">
                  {acceptedTypes.map(type => type.split('/')[1].toUpperCase()).join(', ')} files only
                </p>
                <p className="text-muted-foreground text-xs">
                  Maximum file size: {formatFileSize(maxSize)}
                </p>
              </div>
            )}
          </div>
        </div>

        {isUploading && (
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Uploading...</span>
              <span>{uploadProgress}%</span>
            </div>
            <Progress value={uploadProgress} className="h-2" />
          </div>
        )}

        <div className="flex items-start gap-2 p-3 bg-muted/50 rounded-lg">
          <AlertCircle className="w-4 h-4 text-muted-foreground mt-0.5 flex-shrink-0" />
          <div className="text-xs text-muted-foreground">
            <p className="font-medium mb-1">Supported formats:</p>
            <ul className="space-y-1">
              <li>• PDF files (.pdf) - Preferred format</li>
              <li>• Word documents (.docx)</li>
              <li>• Ensure text is selectable (not scanned images)</li>
            </ul>
          </div>
        </div>
      </div>
    </Card>
  );
};